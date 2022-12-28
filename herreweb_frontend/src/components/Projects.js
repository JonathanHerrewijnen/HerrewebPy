import React, { Component } from "react"
import '../static/Projects.css';

const projectItems = [
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
                <div className="projects-grid-container">
                    {this.state.projectItems.map(item => (
                        <div className="projects-grid-item">
                            <h1>{item.title}</h1>
                            <span>{item.description}</span>
                            <span>{item.rtd_url}</span>
                        </div>
                    ))}
                </div>
            </main>
            // <main className="content">
            //     <div className="row">
            //         <div className="col-md-6 col-sm-10 mx-auto p-0">
            //             <div className="card p-3">
            //                 <ul className="list-group list-group-flush">
            //                     {this.state.projectItems.map(item => (
            //                         <div>
            //                             <h1>{item.title}</h1>
            //                             <span>{item.description}</span>
            //                             <span>{item.rtd_url}</span>
            //                         </div>
            //                     ))}
            //                 </ul>
            //             </div>
            //         </div>
            //     </div>
            // </main>
        )
    }
}

export default Projects;