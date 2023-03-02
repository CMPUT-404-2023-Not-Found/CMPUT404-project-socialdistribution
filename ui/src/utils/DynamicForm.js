import React from 'react'

import { useForm } from 'react-hook-form'
import CheckboxInput from './CheckboxInput';
import SelectInput from './SelectInput';
import TextInput from './TextInput';

/*
    This code was adapted from a video posted by Ian Lenehan on 2022-10-26, retreived on 2023-02-28,
    to YouTube: https://www.youtube.com/watch?v=4oCH5WaJHzk

    I also used the documentation from the react-hook-form website for the components: 
    https://react-hook-form.com/get-started/#Integratinganexistingform

    Got the idea for splitting into components from here:
    https://medium.com/swlh/how-to-generate-dynamic-form-from-json-with-react-5d70386bb38b
*/
const DynamicForm = ({options, formSubmitFunction}) => {
    // PROBLEM
    // properties in the options object must be exactly named as this form expects
    // If a property isn't there, easy to get errors due to accessing null object

    // If we want default values, can add default values 
    // in the options from the backend
    // I think it is relatively easy to pass default values
    // into useForm

    //  variable declarations -------------------------------------
    const { register, handleSubmit } = useForm();

    const textInputs = [];
    const selectInputs = [];
    const checkboxInputs = [];

    if (!options.actions || !options.actions.POST) {
        return (
            <div>
                No form fields provided in OPTIONS
            </div>
        )
    }

    for (let property in options.actions.POST ) {
        let obj = options.actions.POST[property];
        if (obj.read_only === false) {
            if (obj.type === "string") {
                textInputs.push({...obj, "name": property});
            } else if (obj.type === "choice") {
                selectInputs.push({...obj, "name": property});
            } else if (obj.type === "boolean") {
                checkboxInputs.push({...obj, "name": property});
            }
        }
    }

    return (
        <form onSubmit={handleSubmit(formSubmitFunction)}>
            {textInputs.map((textInput, i) => {
                return (
                    <TextInput key={i} register={register} obj={textInput}></TextInput>
                )
            })}

            {selectInputs.map((selectInput, i) => {
                return (
                    <SelectInput key={i} register={register} obj={selectInput}></SelectInput>
                )
            })}

            {checkboxInputs.map((checkboxInput, i) => {
                return (
                    <CheckboxInput key={i} register={register} obj={checkboxInput}></CheckboxInput>
                )
            })}

            <button type="submit" style={{
                marginTop: 15
            }}>Post</button>
        </form>
    )
}

export default DynamicForm
