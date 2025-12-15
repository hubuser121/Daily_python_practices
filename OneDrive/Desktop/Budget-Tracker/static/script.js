/* ==================== API CONFIG ==================== */
const API_BASE_URL = '/api';

/* ==================== CATEGORIES ==================== */
let categories = {
    'Income': [],
    'Expense': []
};

/* ==================== INITIALIZATION ==================== */
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadCategories();
    loadSummary();
    loadTransactions();
    setDefaultDate();
});

function initializeEventListeners() {
    // Tab switching
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', (e) => switchTab(e.target.dataset.tab));
    });

    // Form submission
    document.getElementById('transactionForm').addEventListener('submit', handleAddTransaction);

    // Transaction type change
    document.getElementById('transType').addEventListener('change', updateCategories);

    // Filters
    document.getElementById('filterType').addEventListener('change', filterTransactions);
    document.getElementById('filterCategory').addEventListener('change', filterTransactions);
    document.getElementById('searchBox').addEventListener('input', filterTransactions);
}

/* ==================== TAB SWITCHING ==================== */
function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Deactivate all buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName).classList.add('active');

    // Activate button
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

    // Load specific content
    if (tabName === 'analytics') {
        loadAnalytics();
    } else if (tabName === 'charts') {
        loadCharts();
    }
}

/* ==================== CATEGORIES ==================== */
async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}/categories`);
        categories = await response.json();
        updateCategories();
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

function updateCategories() {
    const transType = document.getElementById('transType').value;
    const categorySelect = document.getElementById('category');
    
    categorySelect.innerHTML = '<option value="">Select Category</option>';
    
    if (transType && categories[transType]) {
        categories[transType].forEach(cat => {
            const option = document.createElement('option');
            option.value = cat;
            option.textContent = cat;
            categorySelect.appendChild(option);
        });
    }

    // Update filter categories
    const filterCategory = document.getElementById('filterCategory');
    const currentValue = filterCategory.value;
    filterCategory.innerHTML = '<option value="">All Categories</option>';
    
    Object.values(categories).flat().forEach(cat => {
        if (!filterCategory.querySelector(`option[value="${cat}"]`)) {
            const option = document.createElement('option');
            option.value = cat;
            option.textContent = cat;
            filterCategory.appendChild(option);
        }
    });
}

/* ==================== DATE HANDLING ==================== */
function setDefaultDate() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').value = today;
}

/* ==================== TRANSACTIONS ==================== */
async function handleAddTransaction(e) {
    e.preventDefault();

    const type = document.getElementById('transType').value;
    const category = document.getElementById('category').value;
    const amount = document.getElementById('amount').value;
    const description = document.getElementById('description').value;
    const date = document.getElementById('date').value;

    if (!type || !category || !amount) {
        showNotification('Please fill in all required fields', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/transactions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: type,
                category: category,
                amount: parseFloat(amount),
                description: description,
                date: date
            })
        });

        if (!response.ok) {
            throw new Error('Failed to add transaction');
        }

        const data = await response.json();
        showNotification('Transaction added successfully!', 'success');
        
        // Reset form
        document.getElementById('transactionForm').reset();
        setDefaultDate();
        
        // Reload data
        loadTransactions();
        loadSummary();
        loadAnalytics();
    } catch (error) {
        console.error('Error:', error);
        showNotification('Failed to add transaction', 'error');
    }
}

async function loadTransactions() {
    try {
        const response = await fetch(`${API_BASE_URL}/transactions`);
        const transactions = await response.json();
        displayTransactions(transactions);
    } catch (error) {
        console.error('Error loading transactions:', error);
    }
}

function displayTransactions(transactions) {
    const container = document.getElementById('transactionsList');
    
    if (transactions.length === 0) {
        container.innerHTML = '<p class="empty-state">No transactions yet. Add one to get started!</p>';
        return;
    }

    container.innerHTML = transactions.reverse().map(trans => `
        <div class="transaction-item ${trans.type.toLowerCase()}">
            <div class="transaction-info">
                <div class="transaction-header">
                    <span class="transaction-category">${trans.category}</span>
                    <span class="transaction-date">${trans.date}</span>
                </div>
                <div class="transaction-description">${trans.description || 'No description'}</div>
            </div>
            <div class="transaction-amount ${trans.type.toLowerCase()}">
                ${trans.type === 'Income' ? '+' : '-'}$${trans.amount.toFixed(2)}
            </div>
            <button class="btn btn-danger" onclick="deleteTransaction('${trans.id}')">Delete</button>
        </div>
    `).join('');
}

async function deleteTransaction(transId) {
    if (!confirm('Are you sure you want to delete this transaction?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/transactions/${transId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Failed to delete transaction');
        }

        showNotification('Transaction deleted successfully!', 'success');
        loadTransactions();
        loadSummary();
        loadAnalytics();
    } catch (error) {
        console.error('Error:', error);
        showNotification('Failed to delete transaction', 'error');
    }
}

function filterTransactions() {
    const type = document.getElementById('filterType').value;
    const category = document.getElementById('filterCategory').value;
    const search = document.getElementById('searchBox').value.toLowerCase();

    const items = document.querySelectorAll('.transaction-item');
    let visibleCount = 0;

    items.forEach(item => {
        let visible = true;

        if (type && !item.classList.contains(type.toLowerCase())) {
            visible = false;
        }

        if (category) {
            const itemCategory = item.querySelector('.transaction-category').textContent;
            if (itemCategory !== category) {
                visible = false;
            }
        }

        if (search) {
            const itemText = item.textContent.toLowerCase();
            if (!itemText.includes(search)) {
                visible = false;
            }
        }

        item.style.display = visible ? 'flex' : 'none';
        if (visible) visibleCount++;
    });

    if (visibleCount === 0) {
        const container = document.getElementById('transactionsList');
        if (!container.querySelector('.empty-state')) {
            const emptyMsg = document.createElement('p');
            emptyMsg.className = 'empty-state';
            emptyMsg.textContent = 'No transactions match your filters.';
            container.appendChild(emptyMsg);
        }
    }
}

/* ==================== SUMMARY ==================== */
async function loadSummary() {
    try {
        const response = await fetch(`${API_BASE_URL}/summary`);
        const data = await response.json();

        document.getElementById('totalIncome').textContent = `$${data.total_income.toFixed(2)}`;
        document.getElementById('totalExpense').textContent = `$${data.total_expense.toFixed(2)}`;
        
        const balance = data.balance;
        const balanceElement = document.getElementById('balance');
        balanceElement.textContent = `$${balance.toFixed(2)}`;
        balanceElement.style.color = balance >= 0 ? '#4CAF50' : '#f44336';
    } catch (error) {
        console.error('Error loading summary:', error);
    }
}

/* ==================== ANALYTICS ==================== */
async function loadAnalytics() {
    try {
        const response = await fetch(`${API_BASE_URL}/summary`);
        const data = await response.json();

        // Expenses by category
        const expensesContainer = document.getElementById('expensesByCategory');
        if (Object.keys(data.expenses_by_category).length === 0) {
            expensesContainer.innerHTML = '<p class="empty-state">No expense data</p>';
        } else {
            expensesContainer.innerHTML = Object.entries(data.expenses_by_category)
                .map(([category, amount]) => `
                    <div class="category-item">
                        <span class="category-name">${category}</span>
                        <span class="category-amount">$${amount.toFixed(2)}</span>
                    </div>
                `).join('');
        }

        // Income by category
        const incomeContainer = document.getElementById('incomeByCategory');
        if (Object.keys(data.income_by_category).length === 0) {
            incomeContainer.innerHTML = '<p class="empty-state">No income data</p>';
        } else {
            incomeContainer.innerHTML = Object.entries(data.income_by_category)
                .map(([category, amount]) => `
                    <div class="category-item">
                        <span class="category-name">${category}</span>
                        <span class="category-amount">$${amount.toFixed(2)}</span>
                    </div>
                `).join('');
        }

        // Monthly summary
        const monthlyContainer = document.getElementById('monthlySummary');
        if (Object.keys(data.monthly_summary).length === 0) {
            monthlyContainer.innerHTML = '<p class="empty-state">No monthly data</p>';
        } else {
            monthlyContainer.innerHTML = Object.entries(data.monthly_summary)
                .map(([month, summary]) => `
                    <div class="monthly-item">
                        <div>
                            <div class="monthly-month">${month}</div>
                            <div class="monthly-details">
                                Income: $${summary.income.toFixed(2)} | Expenses: $${summary.expense.toFixed(2)}
                            </div>
                        </div>
                        <div class="monthly-amount">$${(summary.income - summary.expense).toFixed(2)}</div>
                    </div>
                `).join('');
        }
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

/* ==================== CHARTS ==================== */
async function loadCharts() {
    try {
        // Load pie chart
        const pieImg = document.getElementById('pieChart');
        const pieMsg = document.getElementById('pieChartMessage');
        pieImg.src = `${API_BASE_URL}/charts/expenses-pie?t=${Date.now()}`;
        pieImg.onload = () => {
            pieImg.style.display = 'block';
            pieMsg.style.display = 'none';
        };
        pieImg.onerror = () => {
            pieMsg.textContent = 'No expense data to visualize';
            pieImg.style.display = 'none';
        };

        // Load bar chart
        const barImg = document.getElementById('barChart');
        const barMsg = document.getElementById('barChartMessage');
        barImg.src = `${API_BASE_URL}/charts/monthly-bar?t=${Date.now()}`;
        barImg.onload = () => {
            barImg.style.display = 'block';
            barMsg.style.display = 'none';
        };
        barImg.onerror = () => {
            barMsg.textContent = 'No monthly data to visualize';
            barImg.style.display = 'none';
        };
    } catch (error) {
        console.error('Error loading charts:', error);
    }
}

/* ==================== NOTIFICATIONS ==================== */
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification show ${type}`;

    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}
