// 学生功能相关的 JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('学生脚本已加载');
    
    // 加载学生成绩
    function loadStudentGrades() {
        const tableBody = document.querySelector('#student-grades-table tbody');
        if (!tableBody) return; // 如果表格不存在，直接返回
        
        tableBody.innerHTML = '<tr><td colspan="7" class="text-center"><div class="spinner-border text-primary"></div><p class="mt-2">加载中...</p></td></tr>';
        
        // 这里应该是一个 fetch 请求来获取实际数据
        // 暂时使用示例数据
        setTimeout(() => {
            const grades = [
                { course: '高等数学', score: 88, credit: 4, semester: '2023-2024学年第一学期', teacher: '李老师', date: '2023-12-20' },
                { course: '大学英语', score: 92, credit: 3, semester: '2023-2024学年第一学期', teacher: '王老师', date: '2023-12-18' },
                { course: '数据结构', score: 85, credit: 5, semester: '2023-2024学年第一学期', teacher: '张老师', date: '2023-12-22' }
            ];
            
            renderStudentGrades(grades);
        }, 1000);
    }
    
    // 渲染成绩数据
    function renderStudentGrades(grades) {
        const tableBody = document.querySelector('#student-grades-table tbody');
        if (!tableBody) return;
        
        if (grades.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="7" class="text-center">暂无成绩数据</td></tr>';
            return;
        }
        
        let html = '';
        grades.forEach(grade => {
            html += `
            <tr>
                <td>${grade.course}</td>
                <td>${grade.score}</td>
                <td>${grade.credit}</td>
                <td>${grade.semester}</td>
                <td>${grade.teacher}</td>
                <td>${grade.date}</td>
            </tr>
            `;
        });
        
        tableBody.innerHTML = html;
    }
    
    // 页面初始加载
    const studentGradesTable = document.querySelector('#student-grades-table');
    if (studentGradesTable) {
        loadStudentGrades();
    }
    
    // 注册菜单点击事件处理
    const myGradesLink = document.querySelector('.nav-link[data-module="my-grades"]');
    if (myGradesLink) {
        myGradesLink.addEventListener('click', function() {
            loadStudentGrades();
        });
    }
}); 