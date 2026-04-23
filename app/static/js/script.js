const hamBurgurBtn = document.querySelector('#menu-toggle');
const dropdownBox = document.querySelector("#dropdown");

hamBurgurBtn.addEventListener('click', () => {
    hamBurgurBtn.style.borderRadius = hamBurgurBtn.style.borderRadius === '50%' ? '8px' : '50%';
    dropdownBox.style.display = dropdownBox.style.display === 'flex' ? 'none' : 'flex';
})

document.addEventListener('click', (e) => {
    console.log(e.target);
    if (e.target != hamBurgurBtn && e.target != dropdownBox) {
        dropdownBox.style.display = 'none';
        hamBurgurBtn.style.borderRadius = '8px';
    }
})