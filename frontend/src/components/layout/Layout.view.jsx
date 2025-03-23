import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Button, Layout, Menu } from 'antd';
import {
    HomeFilled,
    LeftOutlined,
    RightOutlined,
    FileTextOutlined,
    FolderOutlined,
    ClockCircleOutlined,
    ClockCircleFilled,
    HomeOutlined,
    RedoOutlined,
} from '@ant-design/icons';
import { getPageHeading, getTasksMenuItems } from '../../utils';

const { Sider, Content } = Layout;

import Logo from '../../assets/logo.jpeg';
import { PATH_NAMES } from '../../constants';
import taskStore from '../../store';

const LayoutView = ({ collapsed, setCollapsed, children }) => {
    const navigate = useNavigate();
    const location = useLocation();
    const { tasks, fetchTasks } = taskStore();
    const taskMenuItems = getTasksMenuItems(tasks);

    return (
        <Layout
            className="h-[100vh] p-0 m-0 flex"
            style={{
                backgroundColor: '#fff',
            }}
        >
            {/* Sidebar with margin and proper height */}
            <div className="m-4 h-[calc(100vh-30px)] flex relative">
                <Sider
                    className="rounded-[20px] h-full    
"
                    style={{
                        backdropFilter: 'blur(10px)', // Frosted glass effect
                        backgroundColor: 'rgba(243, 244, 246, 0.8)',
                        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)', // Soft shadow for depth
                        border: '1px solid rgba(161, 161, 161, 0.3)', // Subtle white border
                        borderRadius: '20px', // Smooth, modern corners
                    }}
                    trigger={null}
                    collapsible
                    collapsed={collapsed}
                >
                    <div
                        className="w-full justify-center items-center flex p-4 cursor-pointer"
                        onClick={() => navigate(PATH_NAMES.DASHBOARD)}
                    >
                        <img className="w-8" src={Logo} alt="Logo" />
                        {!collapsed && (
                            <span
                                className="ml-2 font-semibold text-lg"
                                style={{
                                    color: '#333',
                                    whiteSpace: 'nowrap',
                                    transition: 'opacity 0.3s ease-in-out',
                                }}
                            >
                                Premji Invest
                            </span>
                        )}
                    </div>
                    <div
                        style={{
                            flex: 1,
                            overflowY: 'auto', // Enables vertical scrolling
                            maxHeight: 'calc(100vh - 100px)', // Adjust height dynamically
                        }}
                    >
                        <Menu
                            style={{
                                backgroundColor: 'rgba(227, 242, 253, 0)',
                                border: 'none',
                            }}
                            mode="inline"
                            className="[&_.ant-menu-item-selected]:!bg-[#fff] [&_.ant-menu-item-selected]:!text-[rgba(0,0,0,0.88)] [&_.ant-menu-submenu-selected]:!text-[rgba(0,0,0,0.88)] [&_.ant-menu-submenu-title]:!text-[rgba(0,0,0,0.88)]"
                            selectedKeys={[location.pathname]}
                            defaultOpenKeys={[PATH_NAMES.TASK_DETAIL_BASE]}
                            onClick={({ key }) => navigate(key)}
                            items={[
                                {
                                    key: PATH_NAMES.DASHBOARD,

                                    icon:
                                        location.pathname ===
                                        PATH_NAMES.DASHBOARD ? (
                                            <HomeFilled />
                                        ) : (
                                            <HomeOutlined />
                                        ),

                                    label: 'Home',
                                },
                                {
                                    key: PATH_NAMES.ALL_TASKS,

                                    icon:
                                        location.pathname ===
                                        PATH_NAMES.ALL_TASKS ? (
                                            <ClockCircleFilled />
                                        ) : (
                                            <ClockCircleOutlined />
                                        ),

                                    label: 'Task History',
                                },

                                {
                                    key: PATH_NAMES.TASK_DETAIL_BASE,
                                    icon: <FolderOutlined />,
                                    label: 'Threads',
                                    children: [
                                        ...(taskMenuItems?.map((item) => ({
                                            ...item,
                                            icon: <FileTextOutlined />,
                                        })) || []),
                                    ],
                                },
                            ]}
                        />
                    </div>
                </Sider>
                <div>
                    <Button
                        className="absolute top-8 right-3 z-10 !outline-none !shadow-none
               hover:!bg-gray-200 focus:!bg-white active:!bg-gray-300 
               "
                        shape="circle"
                        icon={
                            collapsed ? (
                                <RightOutlined className="!text-black hover:!text-black focus:!text-black" />
                            ) : (
                                <LeftOutlined className="!text-black hover:!text-black focus:!text-black" />
                            )
                        }
                        onClick={() => setCollapsed(!collapsed)}
                        style={{
                            zIndex: 1000,
                            fontSize: '18px',
                            boxShadow: 'none', // Remove blue glow
                            outline: 'none', // Remove outline focus
                            border: '#ccc .25px solid', // Remove any border effects
                            backgroundColor: '#fff', // Set a default background color
                        }}
                    />
                </div>
            </div>

            {/* Main Layout Content */}
            <Layout className="flex-1 p-0 m-0 h-[100vh] flex flex-col">
                {/* Header with rounded corners & limited width */}
                <div className="flex items-center justify-between  pt-10  bg-[#fff]  ">
                    <h1 className="text-3xl font-bold ">
                        {getPageHeading(location.pathname)}
                    </h1>
                    {location.pathname.includes(
                        PATH_NAMES.TASK_DETAIL_BASE
                    ) && (
                        <div className="pr-20">
                            <Button
                                onClick={() => navigate(PATH_NAMES.ALL_TASKS)}
                            >
                                Go to All tasks
                            </Button>
                        </div>
                    )}

                    {location.pathname.includes(PATH_NAMES.ALL_TASKS) && (
                        <div className="pr-20">
                            <Button
                                onClick={() => fetchTasks()}
                                icon={<RedoOutlined />}
                            >
                                Refetch Tasks
                            </Button>
                        </div>
                    )}

                    {/* side header */}
                    {/* <Header className="rounded-[20px] flex items-center justify-between ">
                         
                    </Header> */}
                </div>

                {/* Content Area */}
                <Content
                    style={{
                        padding: '24px 24px 24px 0px',
                        minHeight: 'calc(100vh - 80px)', // Adjusted for header
                        backgroundColor: '#fff',
                    }}
                >
                    {children}
                </Content>
            </Layout>
        </Layout>
    );
};

export default LayoutView;
