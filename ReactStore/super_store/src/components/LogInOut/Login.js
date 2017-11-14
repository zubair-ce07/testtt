import React from 'react'
import {login} from '../authentication/auth'

class Login extends React.Component {
    constructor(){
        super()
        this.state = {email: '', password: ''}

        this.handleSubmit = this.handleSubmit.bind(this)
        this.handleChange = this.handleChange.bind(this)
    }
    handleSubmit(e) {
        e.preventDefault()
        console.log();
        const that = this;
        var username = this.state.email
        var pass = this.state.password
        login(username, pass, (jsonData) => {
            localStorage.token = jsonData.token;
            that.props.history.push('/home/brands')
        })
    }
    handleChange(e){
        let name = e.target.name
        console.log(e.target.name)
        this.setState({
            [name]: e.target.value
        })
    }
    render() {
        return (
            <div className="container">
                <form onSubmit={this.handleSubmit} className="form-group">
                    <div>
                        email:
                        <input type="text" value={this.state.email} placeholder="username" name="email" onChange={this.handleChange}/>
                    </div>
                    <div>
                        password:
                        <input type="password" value={this.state.password} placeholder="password" name="password" onChange={this.handleChange}/>
                    </div>
                    <input type="submit"/>
                </form>
            </div>
        )
    }
}
export default Login
