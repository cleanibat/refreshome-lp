module.exports = {
  content: ['index.html', '*/index.html', 'assets/site.js'],
  css: ['assets/site.css'],
  output: 'tools/purged',
  fontFace: false,
  keyframes: true,
  variables: false,
  dynamicAttributes: ['data-sticky', 'data-transparent-row', 'data-panel', 'data-header', 'aria-expanded', 'inert', 'data-row', 'aria-modal', 'data-device', 'dir'],
  safelist: {
    standard: ['e-lazyloaded', 'animated', 'slideInUp', 'elementor-invisible', 'ct-active', 'active', 'uc-item-active', 'dropdown-active', 'elementor-active', 'dark', 'jumbo'],
    greedy: [/swiper/, /^elementor-swiper/, /^e-lazyloaded/, /^animated/],
  },
};
