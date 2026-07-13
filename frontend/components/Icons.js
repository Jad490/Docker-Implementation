// SVG Icon Components
const MessageCircle = ({ className = "icon" }) => (
    <svg className={className} viewBox="0 0 24 24">
        <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
    </svg>
);

const Send = ({ className = "icon" }) => (
    <svg className={className} viewBox="0 0 24 24">
        <path d="M22 2L11 13"/>
        <path d="M22 2L15 22L11 13L2 9L22 2Z"/>
    </svg>
);

const CheckCircle = ({ className = "icon" }) => (
    <svg className={className} viewBox="0 0 24 24">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
        <path d="M22 4L12 14.01L9 11.01"/>
    </svg>
);

const XCircle = ({ className = "icon" }) => (
    <svg className={className} viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10"/>
        <path d="M15 9L9 15"/>
        <path d="M9 9L15 15"/>
    </svg>
);

const Loader2 = ({ className = "icon spin" }) => (
    <svg className={className} viewBox="0 0 24 24">
        <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
    </svg>
);

const Heart = ({ className = "icon-lg" }) => (
    <svg className={className} viewBox="0 0 24 24" style={{color: '#ec4899'}}>
        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
    </svg>
);

const ThumbsUp = ({ className = "icon" }) => (
    <svg className={className} viewBox="0 0 24 24">
        <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/>
    </svg>
);

const ThumbsDown = ({ className = "icon" }) => (
    <svg className={className} viewBox="0 0 24 24">
        <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17"/>
    </svg>
);