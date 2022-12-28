import React, { Component } from "react"

const projectItems = [
    {
        id: 1,
        title: "Thelendar",
        description: "Stronghold Kingdoms",
        completed: 1
    },

    {
        id: 2,
        title: "Ghidra Assistant",
        description: "Reversing tools for Ghidra",
        completed: 0
    },

    {
        id: 3,
        title: "Kerk Tallies",
        description: "Creating Tally lights for Church",
        completed: 0
    },
];

class Projects extends Component {
    constructor(props) {
        super(props);
        this.state = { projectItems }
    };

    async componentDidMount() {
        this.setState({projectItems});
        try {
            const res = await fetch('http://localhost:8000/api/projects/');
            const projectItems = await res.json();
            this.setState({projectItems});
        } catch (e) {
            console.log(e);
        }
    }

    render() {
        return (
            <main className="content">
                <div className="row">
                    <div className="col-md-6 col-sm-10 mx-auto p-0">
                        <div className="card p-3">
                            <ul className="list-group list-group-flush">
                                {this.state.projectItems.map(item => (
                                    <div>
                                        <h1>{item.title}</h1>
                                        <span>{item.description}</span>
                                    </div>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>
            </main>
        )
    }
}

export default Projects;