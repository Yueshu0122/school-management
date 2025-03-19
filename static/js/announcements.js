document.addEventListener('DOMContentLoaded', function() {
    console.log('公告脚本已加载');
    
    // 安全地添加事件监听器的辅助函数
    function addEventListenerSafely(selector, event, handler) {
        const elements = document.querySelectorAll(selector);
        if (elements && elements.length > 0) {
            elements.forEach(el => el.addEventListener(event, handler));
            return true;
        }
        return false;
    }
    
    // 编辑公告按钮事件
    addEventListenerSafely('.edit-announcement', 'click', function() {
        const announcementId = this.getAttribute('data-id');
        // 实现编辑逻辑
        console.log('编辑公告:', announcementId);
    });

    // 删除公告按钮事件
    addEventListenerSafely('.delete-announcement', 'click', function() {
        const announcementId = this.getAttribute('data-id');
        // 实现删除逻辑
        if (confirm('确定要删除这个公告吗？')) {
            console.log('删除公告:', announcementId);
        }
    });

    // 添加公告表单提交事件
    const addAnnouncementForm = document.getElementById('addAnnouncementForm');
    if (addAnnouncementForm) {
        addAnnouncementForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // 实现添加公告的 AJAX 提交逻辑
            console.log('提交新公告');
        });
    }

    // 为所有公告卡片添加动画效果
    const announcements = document.querySelectorAll('.announcement-item');
    announcements.forEach(announcement => {
        announcement.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        announcement.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // 安全地为分页链接添加事件监听器
    addEventListenerSafely('.pagination .page-link', 'click', function(e) {
        console.log('分页链接被点击');
    });

    // 安全地添加搜索功能
    addEventListenerSafely('#announcement-search', 'input', function() {
        const searchTerm = this.value.toLowerCase();
        
        // 获取所有公告卡片
        const announcementCards = document.querySelectorAll('#announcements-list .announcement-card');
        if (!announcementCards || announcementCards.length === 0) return;
        
        // 应用过滤
        let anyVisible = false;
        announcementCards.forEach(card => {
            const title = card.querySelector('.announcement-title')?.textContent.toLowerCase() || '';
            const content = card.querySelector('.announcement-content')?.textContent.toLowerCase() || '';
            const author = card.querySelector('.announcement-author')?.textContent.toLowerCase() || '';
            
            const isVisible = title.includes(searchTerm) || content.includes(searchTerm) || author.includes(searchTerm);
            const container = card.closest('.col-md-6');
            if (container) {
                container.style.display = isVisible ? '' : 'none';
            }
            
            if (isVisible) {
                anyVisible = true;
            }
        });
        
        // 如果没有结果则显示提示
        const announcementsList = document.querySelector('#announcements-list');
        if (announcementsList) {
            if (!anyVisible) {
                const noResults = announcementsList.querySelector('.no-results');
                if (!noResults) {
                    const messageDiv = document.createElement('div');
                    messageDiv.className = 'col-12 text-center no-results';
                    messageDiv.innerHTML = '<p class="text-muted">没有找到匹配的公告</p>';
                    announcementsList.appendChild(messageDiv);
                }
            } else {
                const noResults = announcementsList.querySelector('.no-results');
                if (noResults) {
                    noResults.remove();
                }
            }
        }
    });

    console.log('公告脚本初始化完成');
}); 