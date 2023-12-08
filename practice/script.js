document.addEventListener("DOMContentLoaded", function() {
    let isLeftSidebarOpen = false;
    let isRightSidebarOpen = false;

    const dynamicLeftSidebar = document.getElementById("dynamicLeftSidebar");
    const rightSidebar = document.getElementById("rightSidebar");

    document.getElementById("toggleLeftSidebar").addEventListener("click", function() {
        isLeftSidebarOpen = !isLeftSidebarOpen;
        dynamicLeftSidebar.style.transform = isLeftSidebarOpen ? 'translateX(0)' : 'translateX(-100%)';
    });

    document.getElementById("closeLeftSidebar").addEventListener("click", function() {
        isLeftSidebarOpen = false;
        dynamicLeftSidebar.style.transform = 'translateX(-100%)';
    });

    document.getElementById("toggleRightSidebar").addEventListener("click", function() {
        isRightSidebarOpen = !isRightSidebarOpen;
        rightSidebar.style.transform = isRightSidebarOpen ? 'translateX(0)' : 'translateX(-100%)';
    });

    document.getElementById("closeRightSidebar").addEventListener("click", function() {
        isRightSidebarOpen = false;
        rightSidebar.style.transform = 'translateX(-100%)';
    });
});
