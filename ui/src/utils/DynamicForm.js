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
*/
const DynamicForm = ({options, formSubmitFunction}) => {

    // If we want default values, can add default values 
    // in the options from the backend
    // I think it is relatively easy to pass default values
    // into useForm

    const { register, handleSubmit } = useForm();

    const textInputs = [];
    const selectInputs = [];
    const checkboxInputs = [];

    console.log('what');
    console.log(options);
    if (options) console.log(options.actions);

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
