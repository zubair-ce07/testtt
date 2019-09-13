import React from 'react'
import { Link } from 'react-router-dom'

const Signup = () => {
    let card_style = {
        marginTop: '15%'
    }
    return (
        <div className='container'>
            <div className="card" style={card_style}>
                <div className="card-body">
                    <center><h2>Sign Up</h2></center>
                    <form>
                        <div className="form-group">
                            <label htmlFor="exampleUsername">Username</label>
                            <input required type="text" className="form-control" name='username' id="exampleUsername" aria-describedby="emailHelp" placeholder="Enter username" />
                        </div>
                        <div className="form-group">
                            <label htmlFor="exampleInputEmail1">Username</label>
                            <input required type="email" className="form-control" name='username' id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter Email" />
                        </div>
                        <div className="form-group">
                            <label htmlFor="exampleInputPassword1">Password</label>
                            <input required type="password" className="form-control" id="exampleInputPassword1" placeholder="Password" />
                        </div>
                        <div className="form-group">
                            <label htmlFor="exampleInputPassword1">Confrim Password</label>
                            <input required type="password" className="form-control" id="exampleInputPassword1" placeholder="Password" />
                        </div>
                        <button type="submit" className="btn btn-primary">Sign Up</button>
                        <br /><br />
                        <Link to='/login'>Login</Link>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default Signup