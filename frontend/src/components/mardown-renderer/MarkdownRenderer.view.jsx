import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkBreaks from 'remark-breaks';
const MarkdownRendererView = ({ content, styles = {} }) => {
    return (
        <ReactMarkdown
            remarkPlugins={[remarkBreaks]}
            components={{
                h1: (props) => <h1 style={styles.h1} {...props} />,
                h2: (props) => <h2 style={styles.h2} {...props} />,
                h3: (props) => <h3 style={styles.h3} {...props} />,
                h4: (props) => <h4 style={styles.h4} {...props} />,
                h5: (props) => <h5 style={styles.h5} {...props} />,
                h6: (props) => <h6 style={styles.h6} {...props} />,
                p: (props) => <p style={styles.p} {...props} />,
                ul: (props) => <ul style={styles.ul} {...props} />,
                ol: (props) => <ol style={styles.ol} {...props} />,
                li: (props) => <li style={styles.li} {...props} />,
                blockquote: (props) => (
                    <blockquote style={styles.blockquote} {...props} />
                ),
                code: ({ inline, children, ...props }) =>
                    inline ? (
                        <code style={styles.inlineCode} {...props}>
                            {children}
                        </code>
                    ) : (
                        <pre style={styles.codeBlock} {...props}>
                            {children}
                        </pre>
                    ),
            }}
        >
            {content}
        </ReactMarkdown>
    );
};

export default MarkdownRendererView;
