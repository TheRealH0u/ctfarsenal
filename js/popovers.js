document.addEventListener("DOMContentLoaded", () => {
    // Initialize all popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl, {
        // Optional: Customize popover options
    }));

    popoverTriggerList.forEach(trigger => {
        const installationType = trigger.getAttribute('data-installation');
        const customClass = `popover-${installationType}-header`;

        trigger.addEventListener('shown.bs.popover', () => {
            const popoverElement = document.querySelector('.popover');
            if (popoverElement) {
                const popoverHeader = popoverElement.querySelector('.popover-header');
                if (popoverHeader) {
                    popoverHeader.classList.add(customClass);
                }
            }
        });

        trigger.addEventListener('hidden.bs.popover', () => {
            const popoverElement = document.querySelector('.popover');
            if (popoverElement) {
                const popoverHeader = popoverElement.querySelector('.popover-header');
                if (popoverHeader) {
                    popoverHeader.classList.remove(customClass);
                }
            }
        });
    });
});
