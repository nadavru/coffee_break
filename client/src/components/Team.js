import { Component } from 'react';
import { Menu } from 'antd';
import {
    Link
} from "react-router-dom";

class Teams extends Component {
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
                <Menu.Item key="lava">
                    <Link to="/lava">
                        Lava team
                    </Link>
                </Menu.Item>
                <Menu.Item key="java" >
                    <Link to="/java">
                        Java team
                    </Link>
                </Menu.Item>
                <Menu.Item key="yava" >
                    <Link to="/yava">
                        Yava team
                    </Link>
                </Menu.Item>
                <Menu.Item key="bava" >
                    <Link to="/bava">
                        Bava team
                    </Link>
                </Menu.Item>
            </Menu >
        );
    }
}

export default Teams;