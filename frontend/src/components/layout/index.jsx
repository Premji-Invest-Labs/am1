import React, { useState } from 'react';
import LayoutView from './Layout.view';

const LayoutController = ({ children }) => {
    const [collapsed, setCollapsed] = useState(false);
    return (
        <LayoutView collapsed={collapsed} setCollapsed={setCollapsed}>
            {children}
        </LayoutView>
    );
};

export default LayoutController;
