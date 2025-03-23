import { notification } from 'antd';
import React from 'react';

const NotificationController = () => {
    const [notificationApi, contextHolder] = notification.useNotification();
    const [activeNotification, setActiveNotification] = React.useState(null);

    // Configure global notification settings
    React.useEffect(() => {
        notification.destroy(); // Clear any existing notifications on mount
        notification.config({
            maxCount: 1,
            duration: 3, // Default duration in seconds for all notifications
        });
    }, []);

    const openNotification = React.useCallback(
        (type, message = 'Notification', description = '', duration = 3) => {
            if (!notificationApi || !notificationApi[type]) {
                console.error('Notification API not available');
                return;
            }

            // Destroy any existing notification
            if (activeNotification) {
                notification.destroy(activeNotification);
            }

            // Create new notification
            const key = `notification-${Date.now()}`;
            notificationApi[type]({
                message,
                description,
                placement: 'topRight',
                duration,
                key,
                className: `notification-${type}`,
                style: {
                    borderRadius: '8px',
                },
                onClose: () => setActiveNotification(null),
            });

            setActiveNotification(key);
        },
        [notificationApi, activeNotification]
    );

    return { openNotification, contextHolder };
};

export default NotificationController;
