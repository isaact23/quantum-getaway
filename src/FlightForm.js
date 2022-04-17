import React from 'react';
import {Button, Container, Dropdown, DropdownButton, FormControl, InputGroup} from "react-bootstrap";

let CITIES = {0: "New York, NY", 1: "Los Angeles, CA", 2: "Chicago, IL", 3: "Houston, TX", 4: "Phoenix, AZ",
    5: "Philadelphia, PA", 6: "San Antonio, TX", 7: "San Diego, CA", 8: "Dallas, TX", 9: "San Jose, CA",
    10: "Austin, TX", 11: "Jacksonville, FL", 12: "Fort Worth, TX", 13: "Columbus, OH", 14: "Indianapolis, IN",
    15: "Charlotte, NC", 16: "San Francisco, CA", 17: "Seattle, WA", 18: "Denver, CO", 19: "Washington D.C."};

export default class FlightForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            origin: -1,
            destination: -1,
        }
        this.onClickHandler.bind(this);
        this.getOriginText.bind(this);
        this.getDestinationText.bind(this);
    }

    // Handle a form click
    onClickHandler(event, city_id, menu) {
        // Origin menu
        if (menu === 0) {
            this.setState({
                origin: city_id,
            });
        }
        // Destination menu
        else if (menu === 1) {
            this.setState({
                destination: city_id,
            });
        }
        // Submit button press
        else if (menu === 3) {
            this.props.history.push("/results");
        }
    }

    // Get the text for the origin dropdown
    getOriginText() {
        if (this.state.origin < 0) {
            return "Select city"
        }
        return CITIES[this.state.origin];
    }

    // Get the text for the destination dropdown
    getDestinationText() {
        if (this.state.destination < 0) {
            return "Select city"
        }
        return CITIES[this.state.destination];
    }

    render() {
        return (
            <Container>
                <InputGroup size="lg" className="input-group">
                    <InputGroup.Text>Leaving from:</InputGroup.Text>
                    <DropdownButton
                        variant="outline-secondary"
                        title={this.getOriginText()}
                        id="leaving-from"
                    >
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 0, 0)}>New York, NY</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 1, 0)}>Los Angeles, CA</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 2, 0)}>Chicago, IL</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 3, 0)}>Houston, TX</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 4, 0)}>Phoenix, AZ</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 5, 0)}>Philadelphia, PA</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 6, 0)}>San Antonio, TX</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 7, 0)}>San Diego, CA</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 8, 0)}>Dallas, TX</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 9, 0)}>San Jose, CA</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 10,0)}>Austin, TX</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 11,0)}>Jacksonville, FL</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 12,0)}>Fort Worth, TX</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 13,0)}>Columbus, OH</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 14,0)}>Indianapolis, IN</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 15,0)}>Charlotte, NC</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 16,0)}>San Francisco, CA</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 17,0)}>Seattle, WA</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 18,0)}>Denver, CO</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 19,0)}>Washington D.C.</Dropdown.Item>
                    </DropdownButton>
                </InputGroup>
                <InputGroup size="lg" className="input-group">
                    <InputGroup.Text>Going to:</InputGroup.Text>
                    <DropdownButton
                        variant="outline-secondary"
                        title={this.getDestinationText()}
                        id="going to"
                    >
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 0, 1)}>New York, NY</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 1, 1)}>Los Angeles, CA</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 2, 1)}>Chicago, IL</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 3, 1)}>Houston, TX</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 4, 1)}>Phoenix, AZ</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 5, 1)}>Philadelphia, PA</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 6, 1)}>San Antonio, TX</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 7, 1)}>San Diego, CA</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 8, 1)}>Dallas, TX</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 9, 1)}>San Jose, CA</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 10,1)}>Austin, TX</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 11,1)}>Jacksonville, FL</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 12,1)}>Fort Worth, TX</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 13,1)}>Columbus, OH</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 14,1)}>Indianapolis, IN</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 15,1)}>Charlotte, NC</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 16,1)}>San Francisco, CA</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 17,1)}>Seattle, WA</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 18,1)}>Denver, CO</Dropdown.Item>
                        <Dropdown.Item onClick={event => this.onClickHandler(event, 19,1)}>Washington D.C.</Dropdown.Item>
                    </DropdownButton>
                </InputGroup>
                <InputGroup size="lg" className="input-group">
                    <InputGroup.Text>DWave API Key:</InputGroup.Text>
                    <FormControl placeholder="Leave blank for simulated annealing" />
                </InputGroup>
                <InputGroup size="lg" className="input-group">
                    <Button variant="primary" onClick={event => this.onClickHandler(event, -1, 3)}>Find flights</Button>
                </InputGroup>
            </Container>
        );
    }
}
