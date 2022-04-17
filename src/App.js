import './App.scss';

import React from 'react';
import {
    Button,
    Container,
    Dropdown,
    DropdownButton,
    FormControl,
    FormLabel,
    InputGroup,
    Navbar,
    SplitButton
} from "react-bootstrap"

export default class App extends React.Component {
    constructor(props) {
        super(props);
        this.getCities.bind(this);
    }

    getCities() {
        return <>
            <Dropdown.Item>New York, NY</Dropdown.Item>
            <Dropdown.Item>Los Angeles, CA</Dropdown.Item>
            <Dropdown.Item>Chicago, IL</Dropdown.Item>
            <Dropdown.Item>Houston, TX</Dropdown.Item>
            <Dropdown.Item>Phoenix, AZ</Dropdown.Item>
            <Dropdown.Item>Philadelphia, PA</Dropdown.Item>
            <Dropdown.Item>San Antonio, TX</Dropdown.Item>
            <Dropdown.Item>San Diego, CA</Dropdown.Item>
            <Dropdown.Item>Dallas, TX</Dropdown.Item>
            <Dropdown.Item>San Jose, CA</Dropdown.Item>
            <Dropdown.Item>Austin, TX</Dropdown.Item>
            <Dropdown.Item>Jacksonville, FL</Dropdown.Item>
            <Dropdown.Item>Fort Worth, TX</Dropdown.Item>
            <Dropdown.Item>Columbus, OH</Dropdown.Item>
            <Dropdown.Item>Indianapolis, IN</Dropdown.Item>
            <Dropdown.Item>Charlotte, NC</Dropdown.Item>
            <Dropdown.Item>San Francisco, CA</Dropdown.Item>
            <Dropdown.Item>Seattle, WA</Dropdown.Item>
            <Dropdown.Item>Denver, CO</Dropdown.Item>
            <Dropdown.Item>Washington D.C.</Dropdown.Item>
        </>;
    }

    render () {
        return (
            <div className="App">
                <Navbar bg="light" expand="lg">
                    <Container>
                        <Navbar.Brand>Quantum Getaway</Navbar.Brand>
                    </Container>
                </Navbar>
                <Container>
                    <InputGroup size="lg">
                        <FormLabel>Plan your trip</FormLabel>
                        <DropdownButton
                            variant="outline-secondary"
                            title="Leaving from"
                            id="leaving-from"
                        >
                            {this.getCities()}
                        </DropdownButton>
                    </InputGroup>
                    <InputGroup size="lg">
                        <DropdownButton
                            variant="outline-secondary"
                            title="Going to"
                            id="going to"
                        >
                            {this.getCities()}
                        </DropdownButton>
                    </InputGroup>
                    <InputGroup size="lg">
                        <InputGroup.Text>DWave API Key:</InputGroup.Text>
                        <FormControl placeholder="Leave blank for simulated annealing" />
                    </InputGroup>
                    <InputGroup size="lg">
                        <Button variant="primary">Find flights</Button>
                    </InputGroup>
                </Container>
            </div>
        );
    }
}
