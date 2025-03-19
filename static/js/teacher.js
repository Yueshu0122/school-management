/**
 * 教师功能通用JavaScript文件
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('教师模块JS已加载');
    
    // 通用函数：安全地获取CSRF令牌
    window.getCsrfToken = function() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, 'csrftoken'.length + 1) === ('csrftoken=')) {
                    cookieValue = decodeURIComponent(cookie.substring('csrftoken'.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };
    
    // 通用函数：API请求包装器
    window.apiRequest = function(url, method = 'GET', data = null) {
        const csrfToken = window.getCsrfToken();
        const headers = {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        };
        
        const options = {
            method: method,
            headers: headers,
            credentials: 'same-origin' // 包含cookies
        };
        
        if (data && (method === 'POST' || method === 'PUT')) {
            options.body = JSON.stringify(data);
        }
        
        return fetch(url, options)
            .then(response => {
                if (response.status === 401) {
                    console.error('认证失败，请重新登录');
                    // 可以选择重定向到登录页面
                    // window.location.href = '/accounts/login/';
                    return Promise.reject('未授权访问');
                }
                
                if (!response.ok) {
                    return response.json().then(data => {
                        return Promise.reject(data || '请求失败');
                    }).catch(e => {
                        return Promise.reject(`HTTP错误 ${response.status}`);
                    });
                }
                
                return response.json();
            });
    };
    
    // 通用函数：安全地为元素添加事件监听器
    window.addEventListenerSafely = function(selector, event, handler) {
        const elements = document.querySelectorAll(selector);
        if (elements && elements.length > 0) {
            elements.forEach(el => el.addEventListener(event, handler));
            return true;
        }
        return false;
    };
    
    // 通用函数：显示提示消息
    window.showMessage = function(message, type = 'success') {
        // 检查是否存在消息容器，如果不存在则创建
        let messageContainer = document.getElementById('message-container');
        if (!messageContainer) {
            messageContainer = document.createElement('div');
            messageContainer.id = 'message-container';
            messageContainer.style.position = 'fixed';
            messageContainer.style.top = '20px';
            messageContainer.style.right = '20px';
            messageContainer.style.zIndex = '9999';
            document.body.appendChild(messageContainer);
        }
        
        // 创建消息元素
        const messageElement = document.createElement('div');
        messageElement.className = `alert alert-${type} alert-dismissible fade show`;
        messageElement.role = 'alert';
        messageElement.innerHTML = `
            ${message}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        `;
        
        // 添加到容器
        messageContainer.appendChild(messageElement);
        
        // 自动关闭
        setTimeout(() => {
            messageElement.classList.remove('show');
            setTimeout(() => {
                messageContainer.removeChild(messageElement);
            }, 500);
        }, 5000);
    };
}); 