// RiSa Notification System - Custom popup notifications for HR Suite
// Replaces browser alert() with elegant glassmorphism notifications

class NotificationSystem {
    constructor() {
        this.container = this.createContainer();
        this.notifications = [];
        this.initializeStyles();
    }
    
    createContainer() {
        let container = document.getElementById('notificationContainer');
        if (!container) {
            container = document.createElement('div');
            container.className = 'notification-container';
            container.id = 'notificationContainer';
            document.body.appendChild(container);
        }
        return container;
    }
    
    initializeStyles() {
        if (document.getElementById('notification-styles')) return;
        
        const styles = document.createElement('style');
        styles.id = 'notification-styles';
        styles.textContent = `
            .notification-container {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                max-width: 400px;
            }
            
            .custom-notification {
                background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 15px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                transform: translateX(450px);
                transition: all 0.3s ease;
                color: white;
                position: relative;
                overflow: hidden;
                font-family: 'Inter', sans-serif;
            }
            
            .custom-notification.show {
                transform: translateX(0);
            }
            
            .custom-notification::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, #8B5CF6, #3B82F6);
            }
            
            .custom-notification.success::before {
                background: linear-gradient(90deg, #4facfe, #00f2fe);
            }
            
            .custom-notification.error::before {
                background: linear-gradient(90deg, #fa709a, #fee140);
            }
            
            .custom-notification.warning::before {
                background: linear-gradient(90deg, #f6d365, #fda085);
            }
            
            .custom-notification.info::before {
                background: linear-gradient(90deg, #3B82F6, #10B981);
            }
            
            .notification-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 10px;
            }
            
            .notification-title {
                font-weight: 600;
                font-size: 16px;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .notification-close {
                background: none;
                border: none;
                color: rgba(255,255,255,0.7);
                font-size: 18px;
                cursor: pointer;
                padding: 0;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                transition: all 0.2s ease;
            }
            
            .notification-close:hover {
                background: rgba(255,255,255,0.1);
                color: white;
            }
            
            .notification-message {
                font-size: 14px;
                line-height: 1.4;
                opacity: 0.9;
            }
            
            .notification-progress {
                position: absolute;
                bottom: 0;
                left: 0;
                height: 3px;
                background: rgba(255,255,255,0.3);
                transition: width linear;
            }
            
            @media (max-width: 768px) {
                .notification-container {
                    top: 10px;
                    right: 10px;
                    left: 10px;
                    max-width: none;
                }
                
                .custom-notification {
                    transform: translateY(-100px);
                    opacity: 0;
                }
                
                .custom-notification.show {
                    transform: translateY(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(styles);
    }
    
    show(message, type = 'info', title = '', duration = 5000) {
        const id = 'notification_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };
        
        const titles = {
            success: title || 'Success',
            error: title || 'Error',
            warning: title || 'Warning',
            info: title || 'Information'
        };
        
        const notification = document.createElement('div');
        notification.className = `custom-notification ${type}`;
        notification.id = id;
        
        notification.innerHTML = `
            <div class="notification-header">
                <div class="notification-title">
                    <i class="${icons[type]}"></i>
                    ${titles[type]}
                </div>
                <button class="notification-close" onclick="window.risaNotifications.close('${id}')">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="notification-message">${message}</div>
            <div class="notification-progress" id="progress_${id}"></div>
        `;
        
        this.container.appendChild(notification);
        this.notifications.push({ id, element: notification, duration });
        
        // Trigger animation
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        // Auto-close with progress bar
        if (duration > 0) {
            const progressBar = document.getElementById(`progress_${id}`);
            if (progressBar) {
                progressBar.style.width = '100%';
                progressBar.style.transition = `width ${duration}ms linear`;
                
                setTimeout(() => {
                    progressBar.style.width = '0%';
                }, 100);
                
                setTimeout(() => {
                    this.close(id);
                }, duration);
            }
        }
        
        return id;
    }
    
    close(id) {
        const notification = document.getElementById(id);
        if (notification) {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
                this.notifications = this.notifications.filter(n => n.id !== id);
            }, 300);
        }
    }
    
    closeAll() {
        this.notifications.forEach(n => this.close(n.id));
    }
    
    success(message, title = '', duration = 5000) {
        return this.show(message, 'success', title, duration);
    }
    
    error(message, title = '', duration = 7000) {
        return this.show(message, 'error', title, duration);
    }
    
    warning(message, title = '', duration = 6000) {
        return this.show(message, 'warning', title, duration);
    }
    
    info(message, title = '', duration = 5000) {
        return this.show(message, 'info', title, duration);
    }
}

// Initialize global notification system
if (typeof window !== 'undefined') {
    window.risaNotifications = new NotificationSystem();
    
    // Override alert function globally
    window.alert = function(message) {
        // Determine type based on message content
        let type = 'info';
        let cleanMessage = message;
        
        if (message.includes('✅') || message.includes('🎉') || message.includes('successfully') || message.includes('Success')) {
            type = 'success';
        } else if (message.includes('❌') || message.includes('Error') || message.includes('error') || message.includes('failed')) {
            type = 'error';
        } else if (message.includes('⚠️') || message.includes('Warning') || message.includes('warning')) {
            type = 'warning';
        }
        
        // Clean message (remove emojis for cleaner look)
        cleanMessage = message.replace(/[✅❌🎉⚠️📊📅📨🔍💡🛠😂🌀👣]/g, '').trim();
        
        window.risaNotifications.show(cleanMessage, type);
    };
    
    // Add convenience methods to window
    window.showSuccess = (message, title) => window.risaNotifications.success(message, title);
    window.showError = (message, title) => window.risaNotifications.error(message, title);
    window.showWarning = (message, title) => window.risaNotifications.warning(message, title);
    window.showInfo = (message, title) => window.risaNotifications.info(message, title);
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NotificationSystem;
}