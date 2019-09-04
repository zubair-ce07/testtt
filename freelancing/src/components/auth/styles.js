import styled, { css } from "styled-components";

export const Wrapper = styled.div`
  display: flex;
  justify-content: center;
  margin-top: 10px;
  padding: 10px;
`;

export const StyledForm = styled.form`
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 500px;
    padding: 10px;
    background: ${props => props.theme.bg}
    border-radius: 10px;
    box-shadow: 3px ${props => props.theme.accent}
`;

export const FormTitle = styled.p`
  font-size: 24px;
  font-weight: 600;
`;

export const FormRow = styled.div`
  display: flex;
  justify-content: center;
  width: 100%;
  box-sizing: border-box;
  padding: 10px;
  margin: 5px 10px;
`;
export const FormErrorRow = styled(FormRow)`
  flex-direction: column;
  align-items: flex-end;
`;

export const FormInput = styled.input`
    width: 100%;
    box-sizing: border-box;
    padding: 10px 5px;
    border: none;
    color: ${props => props.theme.tint[0]}
    background: white;
    border-radius: 5px;
    font-size: 18px;
    font-family: input-mono, monospace;
    &:focus {
        outline-color: ${props => props.theme.main}
    }

    ${props =>
      props.error &&
      css`
            background: ${props => props.theme.color.tint.red[2]}
            color: ${props => props.theme.bg}
            &:focus {
                outline-color: ${props => props.theme.color.tint.red[0]}
            }
        `}
`;

export const FormButton = styled.button`
  width: 70%;
  padding: 10px;
  border: 2px solid ${props => props.theme.main};
  border-radius: 5px;
  font-size: 18px;
  color: ${props => props.theme.main};
  background-color: ${props => props.theme.bg};
  margin-top: 24px;

  &:hover {
    color: ${props => props.theme.bg};
    background-color: ${props => props.theme.main};
  }
`;

export const FormErrorText = styled.div`
  font-size: 14px;
  color: red;
  font-family: input-mono, monospace;
`;
