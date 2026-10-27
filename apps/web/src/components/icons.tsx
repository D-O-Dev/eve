import type { ReactNode } from "react";

const PATHS = {
    commerce: <><path d="M5 8h14l1 12H4z" /><path d="M9 8V7a3 3 0 0 1 6 0v1" /></>,
    food: <><path d="M6 3v6a2 2 0 0 0 4 0V3M8 11v10" /><path d="M17 21V3c-2.5 1.5-3.5 5-3 8h3" /></>,
    services: <><path d="M4 8h16v11H4z" /><path d="M9 8V6a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2M4 13h16" /></>,
    transport: <><path d="M2 7h11v9H2zM13 10h4l3 3v3h-7" /><circle cx="6" cy="18" r="2" /><circle cx="17" cy="18" r="2" /></>,
    digital: <><path d="M4 5h16v11H4zM2 19h20" /><path d="M10 9l-2 2 2 2M14 9l2 2-2 2" /></>,
    plus: <path d="M12 5v14M5 12h14" />,
    lock: <><rect x="5" y="11" width="14" height="10" rx="2" /><path d="M8 11V8a4 4 0 0 1 8 0v3" /></>,
    palette: <><path d="M12 3a9 9 0 1 0 0 18c1.2 0 2-.8 2-1.8 0-.5-.2-.9-.5-1.2-.3-.3-.5-.7-.5-1.2 0-1 .8-1.8 1.8-1.8H17a4 4 0 0 0 4-4C21 6.4 17 3 12 3z" /><circle cx="7.5" cy="11" r="1" /><circle cx="10" cy="7" r="1" /><circle cx="15" cy="7" r="1" /></>,
} satisfies Record<string, ReactNode>;

export type IconName = keyof typeof PATHS;

export function Icon({ name }: { name: IconName }) {
    return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"
            strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            {PATHS[name]}
        </svg>
    );
}