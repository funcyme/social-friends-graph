(function() {
    let isSelecting = false;
    let selectedElement = null;
    let hoveredElement = null;

    // Start or stop selecting mode
    const toggleSelecting = () => {
        isSelecting = !isSelecting;
        document.body.style.cursor = isSelecting ? 'crosshair' : 'default';

        if (!isSelecting && selectedElement) {
            const uniqueClass = classname;
            selectedElement.classList.add(uniqueClass);
            console.log(`Class "${uniqueClass}" added to the selected element:`, selectedElement);
            selectedElement = null;
        }

        // Remove any outline when turning off selection
        if (!isSelecting && hoveredElement) {
            hoveredElement.style.outline = '';
            hoveredElement = null;
        }

        button.innerText = isSelecting ? 'Cancel Selection' : 'Start Selecting';
    };

    // Handle user clicks to select an element
    document.addEventListener('click', (event) => {
    if (!isSelecting || event.target === button) return;

    event.preventDefault(); // Stop default link navigation
    event.stopPropagation(); // Stop bubbling
    event.stopImmediatePropagation(); // Stop all other handlers

    // If the clicked element is inside a link, stop link behavior
    let el = event.target;
    while (el && el !== document.body) {
        if (el.tagName === 'A' && el.href) {
            el.removeAttribute('href'); // Just in case
            break;
        }
        el = el.parentElement;
    }

    selectedElement = event.target;
    toggleSelecting();
}, true); // capture = true


    // Highlight the hovered element while selecting
    document.addEventListener('mouseover', (event) => {
        if (isSelecting && event.target !== button) {
            if (hoveredElement) {
                hoveredElement.style.outline = '';
            }
            hoveredElement = event.target;
            hoveredElement.style.outline = '3px solid rgba(255, 165, 0, 0.7)';
        }
    });

    // Remove highlight on mouseout
    document.addEventListener('mouseout', (event) => {
        if (isSelecting && hoveredElement) {
            hoveredElement.style.outline = '';
            hoveredElement = null;
        }
    });

    // Create the toggle button
    const button = document.createElement('button');
    button.innerText = 'Start Selecting';
    Object.assign(button.style, {
        position: 'fixed',
        top: '10px',
        left: '10px',
        padding: '10px 15px',
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        color: 'white',
        border: 'none',
        cursor: 'pointer',
        zIndex: '2147483647', // Max safe z-index value
        fontSize: '14px',
        fontFamily: 'sans-serif',
        borderRadius: '4px'
    });

    button.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleSelecting();
    });

    document.body.appendChild(button);
})();
