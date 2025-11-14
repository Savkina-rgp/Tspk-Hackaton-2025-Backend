 const cards = document.querySelectorAll('.card');

cards.forEach(card => {
  card.addEventListener('dragstart', () => {
    card.classList.add('dragging');
  });

  card.addEventListener('dragend', () => {
    card.classList.remove('dragging');
  });
});

const scrollContainers = document.querySelectorAll('.scroll-row');

scrollContainers.forEach(container => {
  let isDown = false;
  let startX;
  let scrollLeft;
  let velocity = 0;
  let momentumID;

  const start = (e) => {
    isDown = true;
    container.classList.add('active');
    startX = e.pageX || e.touches[0].pageX;
    scrollLeft = container.scrollLeft;
    cancelMomentum();
  };

  const move = (e) => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX || e.touches[0].pageX;
    const walk = (x - startX);
    const prevScroll = container.scrollLeft;
    container.scrollLeft = scrollLeft - walk;
    velocity = container.scrollLeft - prevScroll;
  };

  const end = () => {
    isDown = false;
    container.classList.remove('active');
    startMomentum();
  };

  // Инерция (плавное замедление)
  function startMomentum() {
    cancelMomentum();
    momentumID = requestAnimationFrame(momentumLoop);
  }
  function cancelMomentum() {
    cancelAnimationFrame(momentumID);
  }
  function momentumLoop() {
    container.scrollLeft += velocity;
    velocity *= 0.95; // чем меньше число, тем быстрее остановка
    if (Math.abs(velocity) > 0.5) {
      momentumID = requestAnimationFrame(momentumLoop);
    }
  }

  // Мышь
  container.addEventListener('mousedown', start);
  container.addEventListener('mousemove', move);
  container.addEventListener('mouseup', end);
  container.addEventListener('mouseleave', end);

  // Сенсорные экраны
  container.addEventListener('touchstart', start);
  container.addEventListener('touchmove', move);
  container.addEventListener('touchend', end);
});