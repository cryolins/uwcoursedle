import type { Action } from "svelte/action";

export const clickOutside: Action<HTMLDivElement, undefined> = (node) => {
    const handleClick = (event: MouseEvent) => {
        if (node && !node.contains(event.target as Node) && !event.defaultPrevented) {
            node.dispatchEvent(new CustomEvent('click_outside'));
        }
    }

    $effect(() => {
        document.addEventListener('click', handleClick, true);
        return () => {
            document.removeEventListener('click', handleClick, true);
        };
    });
};