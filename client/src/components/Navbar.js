import { Component } from 'react';
import { Menu } from 'antd';
import {
    Link
} from "react-router-dom";

class Navbar extends Component {
    state = {
        current: 'mail',
    };

    handleClick = e => {
        console.log('click ', e);
        this.setState({ current: e.key });
    };

    render() {
        const { current } = this.state;
        return (
            <Menu onClick={this.handleClick} selectedKeys={[current]} mode="horizontal">
                <Menu.Item key="breaks">
                    <Link to="/breaks">
                        Breaks
                    </Link>
                </Menu.Item>
                <Menu.Item key="availability" >
                    <Link to="/availability"> 
                        Availability
                    </Link>
                </Menu.Item>
                <Menu.Item key="calendar" >
                    <Link to="/calendar">
                        Calendar
                    </Link>
                </Menu.Item>
            </Menu >
        );
    }
}

export default Navbar;