import React, { Component } from "react"
import '../static/Projects.css';
import { useNavigate } from "react-router-dom";

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
                        { this.state.projectItems.map(item => (
                            <div className="project-grid-item">
                                <h2>{item.title}</h2>
                                <div></div>
                                <div></div>
                                <div></div>
                                <div></div>
                                { item.url  
                                    ? <div className="project-url-btn">Website</div>
                                    : <div />
                                }
                                { item.rtd_url  
                                    ? <div className="project-rtd-url-btn">Documentation</div>
                                    : <div />
                                }                                
                                <img className="project-image-box" src={item.image}/>
                                <div className="description-box">{item.description}</div>
                                <div></div>
                                <div></div>
                                <div></div>
                                <div></div>
                                <div></div>
                            </div>
                        ))}
                </div>
            </main>
        )
    }
}

export default Projects;