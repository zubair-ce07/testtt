import createStyles from '@material-ui/styles/createStyles';

export const appStyles = () =>
    createStyles({
        cardStyle: {
            margin: '10px',
            width: '100%'
        },
        authCard:{
            marginTop: '15%',
            padding: '20px'
        },
        navBarLink:{
            textDecoration: 'none',
            color:'white'
        },
        routeLink:{
            textDecoration: 'none'
        },
        textFieldStyle: {
            width: '100%'
        },
        navBarContent:{
            float: 'right',
            marginRight:'5px'
        },
        narBarFirstElement:{
            flex:'1'
        },
        timeSlotHeading:{ 
            width: '100%',
            textAlign: 'center' 
        }
    });