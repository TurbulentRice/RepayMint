import { useEffect, useState } from "preact/hooks";

export default function useResize () {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  // const debounce = (func, delay) => {
  //   let timeoutId;
  //   return function () {
  //     const context = this;
  //     const args = arguments;
  //     clearTimeout(timeoutId);
  //     timeoutId = setTimeout(() => {
  //       func.apply(context, args);
  //     }, delay);
  //   };
  // };

  const handleResize = () => {
    setWindowSize({
      width: window.innerWidth,
      height: window.innerHeight,
    });
  };

  useEffect(() => {
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return {
    windowSize,
    isMobile: () => windowSize <= 767,
    isTablet: () => (windowSize <= 1023) && (windowSize >= 768),
    isDesktop: () => windowSize >= 1024
  };
};
