import React, { useState } from 'react';

const TextCellRenderer = (props) => {
    const [expanded, setExpanded] = useState(false);

    const text = props.value || '';

    const words = text.split(' ');
    const truncatedText =
        words.slice(0, 10).join(' ') + (words.length > 10 ? '...' : '');

    // Toggle text expansion on click
    const toggleExpand = () => setExpanded(!expanded);

    return (
        <div
            style={{
                cursor: 'pointer',
                whiteSpace: 'normal',
                wordBreak: 'break-word',
            }}
            onClick={toggleExpand}
        >
            {expanded ? text : truncatedText}
        </div>
    );
};

export default TextCellRenderer;
