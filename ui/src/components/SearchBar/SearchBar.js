import SearchIcon from '@mui/icons-material/Search';
import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';

const SearchBar = ({placeholder, value, onChange, onSearch}) => {
  return (
    <div>
        <TextField
            value={value}
            placeholder={placeholder}
            onChange= {onChange}
        />
        <IconButton
            aria-label="search"
            onClick= {onSearch}
        >
            <SearchIcon/>
        </IconButton>
    </div>
  )
}

export default SearchBar
