import React from 'react'
import { useState } from 'react';
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom';
import CheckboxInput from './CheckboxInput';
import FileInput from './FileInput';
import SelectInput from './SelectInput';
import TextInput from './TextInput';
import Button from '@mui/material/Button';

import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';

/*
    This code was adapted from a video posted by Ian Lenehan on 2022-10-26, retreived on 2023-02-28,
    to YouTube: https://www.youtube.com/watch?v=4oCH5WaJHzk

    I also used the documentation from the react-hook-form website for the components: 
    https://react-hook-form.com/get-started/#Integratinganexistingform

    Got the idea for splitting into components from here:
    https://medium.com/swlh/how-to-generate-dynamic-form-from-json-with-react-5d70386bb38b
*/
const DynamicForm = ({options, formSubmitFunction, defaultobjs}) => {
    // PROBLEM
    // properties in the options object must be exactly named as this form expects
    // If a property isn't there, easy to get errors due to accessing null object

    // If we want default values, can add default values 
    // in the options from the backend
    // I think it is relatively easy to pass default values
    // into useForm

    //  variable declarations -------------------------------------
    const { register, handleSubmit } = useForm({
      defaultValues: {...defaultobjs
      }
    });
    console.log(defaultobjs);
    const textInputs = [];
    const selectInputs = [];
    const checkboxInputs = [];
    const fileInputs = [];
    const [contentType, setContentType] = useState('');

    //  event listeners --------------------------------------------
    const categories = [
      "business",
      "education",
      "entertainment",
      "finance",
      "health",
      "lifestyle",
      "other",
      "science",
      "sports",
      "technology",
      "travel",
      "tutorial",
      "web",
    ];
    const [selectedCategories, setSelectedCategories] = useState([]);
    const [customCategory, setCustomCategory] = useState(null);
    const [customCategoryInput, setCustomCategoryInput] = useState('');
    const [updatedCategories, setUpdatedCategories] = useState(categories);
    const [showCustomCategoryInput, setShowCustomCategoryInput] = useState(false);
    const [customCategoryError, setCustomCategoryError] = useState('');
    const [categoriesError, setCategoriesError] = useState('');
    
    const navigate = useNavigate();


    // Update your onSubmit function to navigate to the stream page
    const onSubmit = (data) => {
      if (selectedCategories.length === 0) {
        setCategoriesError('Please select at least one category.');
      } else {
        setCategoriesError(''); // Clear the error message when categories are selected
        formSubmitFunction({ ...data, categories: selectedCategories });
        navigate('/'); // Navigate to the stream page
      }
    };
    

    const handleCategoriesChange = (event, value) => {
      if (value.includes('other')) {
        setShowCustomCategoryInput(true);
        setCustomCategory('');
      } else {
        setShowCustomCategoryInput(false);
        setCustomCategory(null);
      }
      setSelectedCategories(value.filter((category) => category !== 'other'));
      register('categories').onChange({ target: { value: value.filter((category) => category !== 'other').join(',') } });
    };
    
    const handleAddCustomCategory = () => {
      if (customCategoryInput.trim() === '') {
        setCustomCategoryError('Please enter a non-empty custom category.');
        return;
      }
      const updatedCategoriesWithCustom = [
        ...updatedCategories,
        customCategoryInput,
      ].sort((a, b) => a.localeCompare(b));
      setUpdatedCategories(updatedCategoriesWithCustom);
      setSelectedCategories([...selectedCategories, customCategoryInput]);
      setShowCustomCategoryInput(false);
      setCustomCategoryInput('');
      register('categories').onChange({
        target: { value: selectedCategories.join(',') },
      });
    };
    
    const handleCustomCategoryInputChange = (event) => {
      const regexPattern = /^[a-zA-Z]*$/;
      if (regexPattern.test(event.target.value) && !event.target.value.includes(' ')) {
        setCustomCategoryInput(event.target.value);
        setCustomCategoryError(''); // Clear the error message if the input is valid
      } else {
        // Set an error message for invalid input
        setCustomCategoryError('Please enter a valid category without spaces or special characters.');
      }
    };
    
    
    const handleContentTypeChange = (event) => {
        setContentType(event.target.value);
    };

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
            } else if (obj.type === "file") {
                fileInputs.push({...obj, "name": property})
            }
        }
    }
    console.log(contentType);
    console.log(selectedCategories);
    return (
      <form onSubmit={handleSubmit(onSubmit)}>
          {textInputs.map((textInput, i) => {
            if (i === 1) {
              return (
                <>
                  <TextInput key={i} register={register} obj={textInput} />
                  {selectInputs.map((selectInput, j) => {
                    if (j === 0) {
                      return (
                        <SelectInput
                          key={j}
                          register={register}
                          obj={selectInput}
                          onChange={handleContentTypeChange}
                        />
                      );
                    }
                  })}
                </>
              );
            } else if (i === 2) {
              return (
                <>
                  {contentType === "image/png;base64" || contentType === "image/jpeg;base64" ? (
                    fileInputs.map((fileInput, i) => {
                      return (
                        <FileInput key={i} register={register} obj={fileInput} />
                      );
                    })
                  ) : (
                    <TextInput key={i} register={register} obj={textInput} />
                  )}
                </>
              );
            } else {
              return <TextInput key={i} register={register} obj={textInput} />;
            }
          })}

          <Autocomplete
              multiple
              options={updatedCategories}
              value={selectedCategories}
              onChange={handleCategoriesChange}
              renderInput={(params) => (
                <TextField {...params} label="Categories" 
                InputLabelProps={{
                  style: {
                  fontSize: '18px', // Set the desired font size
                  fontWeight: 'bold',
              },
              }}/>
              )}
            /> 
            {categoriesError && (
              <Typography variant="body2" color="error">
                {categoriesError}
              </Typography>
            )}
              {showCustomCategoryInput && (
                <>
                  <br />
                  <Stack direction="row" alignItems="center" spacing={1}>
                    <TextField
                      label="Custom Category"
                      value={customCategoryInput}
                      onChange={handleCustomCategoryInputChange}
                      error={!!customCategoryError}
                    />
                    <Button
                      onClick={handleAddCustomCategory}
                      variant="contained"
                      color="primary"
                      size="small"
                      disabled={customCategoryInput.trim() === ''}
                    >
                      Add Category
                    </Button>
                  </Stack>
                  {customCategoryError && (
                    <Typography variant="body2" color="error">
                      {customCategoryError}
                    </Typography>
                  )}
                </>
              )}
        
          {selectInputs.map((selectInput, i) => {
            if (i === 1) {
              return (
                <SelectInput key={i} register={register} obj={selectInput} />
              );
            }
          })}
        {checkboxInputs.map((checkboxInput, i) => {
        return (
            <CheckboxInput key={i} register={register} obj={checkboxInput} />
        ); 
        })}
        
        
          <br />
          <Button  type="submit" variant="contained">Post</Button>
        </form>
       
      );   
      
}

export default DynamicForm
