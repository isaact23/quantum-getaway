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
import FlightForm from "./FlightForm";

export default class App extends React.Component {
    constructor(props) {
        super(props);
    }

    render () {
        return (
            <div className="App">
                <Navbar bg="light" expand="lg">
                    <Container>
                        <Navbar.Brand>Quantum Getaway</Navbar.Brand>
                    </Container>
                </Navbar>
                <FlightForm/>
            </div>
        );
    }
}
