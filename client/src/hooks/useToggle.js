import { useState } from "preact/hooks";

// The simplest toggle hook I could imagine
export default function useToggle(initialState = {}) {
  const [toggles, setToggles] = useState(initialState);
  return {
    toggles,
    toggle: (name) => setToggles({...toggles, [name]: !toggles[name]})
  }
}
