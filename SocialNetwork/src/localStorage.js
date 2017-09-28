
export const loadState = () => {
	try{
		const serializedState = localStorage.getItem('authReducer')

		if (serializedState === null){
			return undefined;
		}
		return JSON.parse(serializedState)
	}
	catch(err){
			return undefined;
	}
}

export const saveState = (auth_state) => {
	try{
		const serializedState = JSON.stringify(auth_state);
		localStorage.setItem('authReducer',serializedState);		
	}
	catch(err){
		//return state
	}
}