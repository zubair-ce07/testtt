export const formatDate = date => {
    const options = {year: 'numeric', month: 'long', day: 'numeric'};
    return 'Born: ' + date.toLocaleDateString('en-US', options);
};
