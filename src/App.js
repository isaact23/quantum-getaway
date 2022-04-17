import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
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
import Results from "./Results";

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
                <BrowserRouter>
                    <Routes>
                        <Route path="/">
                            <Route index element={<FlightForm/>}/>
                            <Route path="results" element={<Results/>}/>
                        </Route>
                    </Routes>
                </BrowserRouter>
            </div>
        );
    }
}
