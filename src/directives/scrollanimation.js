// src/directives/scrollanimation.js
export default {
    beforeMount(el) {
      el.classList.add('before-enter');
  
      const animate = () => {
        const rect = el.getBoundingClientRect();
        if (rect.top <= window.innerHeight * 0.75) {
          el.classList.add('enter');
          el.classList.remove('before-enter');
          window.removeEventListener('scroll', animate);
        }
      };
  
      window.addEventListener('scroll', animate);
      animate();
    }
  };
  