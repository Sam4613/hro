/**
 * Authentication utility for HR Suite
 * Handles JWT tokens and API requests
 */

class AuthManager {
    constructor() {
        this.token = localStorage.getItem('hr_token');
        this.user = JSON.parse(localStorage.getItem('hr_user') || 'null');
    }

    // Check if user is authenticated
    isAuthenticated() {
        return !!this.token;
    }

    // Get current user
    getCurrentUser() {
        return this.user;
    }

    // Get auth headers for API requests
    getAuthHeaders() {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        
        return headers;
    }

    // Make authenticated API request
    async apiRequest(url, options = {}) {
        const defaultOptions = {
            headers: this.getAuthHeaders()
        };
        
        const mergedOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...(options.headers || {})
            }
        };
        
        try {
            const response = await fetch(url, mergedOptions);
            
            // Handle authentication errors
            if (response.status === 401) {
                this.logout();
                window.location.href = '/login';
                throw new Error('Authentication required');
            }
            
            return response;
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    }

    // Login user
    async login(email, password) {
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.token = data.token;
                this.user = data.user;
                
                localStorage.setItem('hr_token', this.token);
                localStorage.setItem('hr_user', JSON.stringify(this.user));
                
                return { success: true, user: this.user };
            } else {
                return { success: false, error: data.error };
            }
        } catch (error) {
            console.error('Login error:', error);
            return { success: false, error: 'Network error' };
        }
    }

    // Logout user
    logout() {
        this.token = null;
        this.user = null;
        
        localStorage.removeItem('hr_token');
        localStorage.removeItem('hr_user');
        
        // Optional: Call logout API
        fetch('/api/logout', {
            method: 'POST',
            headers: this.getAuthHeaders()
        }).catch(console.error);
    }

    // Redirect to login if not authenticated
    requireAuth() {
        if (!this.isAuthenticated()) {
            window.location.href = '/login';
            return false;
        }
        return true;
    }

    // Update user info in navbar
    updateNavbar() {
        if (this.user) {
            const userNameElements = document.querySelectorAll('.user-name');
            const userRoleElements = document.querySelectorAll('.user-role');
            const userAvatarElements = document.querySelectorAll('.user-avatar');
            
            userNameElements.forEach(el => el.textContent = this.user.name);
            userRoleElements.forEach(el => el.textContent = this.user.role);
            userAvatarElements.forEach(el => {
                if (el.tagName === 'IMG') {
                    el.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(this.user.name)}&background=32f5c8&color=000&size=40`;
                } else {
                    el.textContent = this.user.name.split(' ').map(n => n[0]).join('').toUpperCase();
                }
            });
        }
    }
}

// Global auth manager instance
const auth = new AuthManager();

// Auto-redirect to login if not authenticated (except on login and landing pages)
if (typeof window !== 'undefined') {
    const currentPath = window.location.pathname;
    const publicPaths = ['/', '/login', '/landing'];
    
    if (!publicPaths.includes(currentPath) && !auth.isAuthenticated()) {
        window.location.href = '/login';
    }
}

// Enhanced API helper functions
window.hrAPI = {
    // Task management
    async createTask(taskData) {
        const response = await auth.apiRequest('/api/tasks', {
            method: 'POST',
            body: JSON.stringify(taskData)
        });
        return response.json();
    },
    
    async getTasks(filters = {}) {
        const params = new URLSearchParams(filters);
        const response = await auth.apiRequest(`/api/tasks?${params}`);
        return response.json();
    },
    
    async updateTaskStatus(taskId, status) {
        const response = await auth.apiRequest(`/api/tasks/${taskId}/status`, {
            method: 'PUT',
            body: JSON.stringify({ status })
        });
        return response.json();
    },
    
    // AI Assistant
    async queryAI(query, voiceInput = false) {
        const response = await auth.apiRequest('/api/ai-query', {
            method: 'POST',
            body: JSON.stringify({ query, voice_input: voiceInput })
        });
        return response.json();
    },
    
    // Attendance
    async checkIn(data) {
        const response = await auth.apiRequest('/api/checkin', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        return response.json();
    },
    
    // Tokens
    async mintTokens(amount, reason) {
        const response = await auth.apiRequest('/api/mint-tokens', {
            method: 'POST',
            body: JSON.stringify({ amount, reason })
        });
        return response.json();
    },
    
    // Location
    async updateLocation(lat, lng, status = 'active') {
        const response = await auth.apiRequest('/api/location/update', {
            method: 'POST',
            body: JSON.stringify({ lat, lng, status })
        });
        return response.json();
    },
    
    async getLiveMap(team = null) {
        const params = team ? `?team=${team}` : '';
        const response = await auth.apiRequest(`/api/location/live-map${params}`);
        return response.json();
    }
};

// Show notification helper
function showNotification(message, type = 'info', duration = 5000) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
    `;
    notification.innerHTML = `
        <div class="d-flex justify-content-between align-items-center">
            <span>${message}</span>
            <button type="button" class="btn-close" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AuthManager, auth };
}