import React from 'react';
import {
    queryStyles,
    ResponseStyles,
} from '../../constants/ReactMarkdownStyles';
import MarkdownRendererView from './MarkdownRenderer.view';
const MarkdownRendererController = ({ content, type = 'response' }) => {
    return (
        <MarkdownRendererView
            content={content}
            styles={type === 'query' ? queryStyles : ResponseStyles}
        />
    );
};

export default MarkdownRendererController;
