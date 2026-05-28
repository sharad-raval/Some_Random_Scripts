import winreg


if __name__ == '__main__':
	key_path = "Software\\Policies\\Microsoft\\Windows\\Explorer"  # Path under HKEY_CURRENT_USER
	value_name = "DisableSearchBoxSuggestions"
	value_data = 1

	try:
		# Use HKEY_LOCAL_MACHINE (Requires Admin) or HKEY_CURRENT_USER (No Admin)
		key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)

		# Set the registry value as DWORD (32-bit integer)
		winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value_data)

		# Close the key
		winreg.CloseKey(key)

		print(f"Successfully added {value_name} as DWORD to {key_path} with value: {value_data}")
	except PermissionError:
		print("Permission denied! Run the script as Administrator.")
	except Exception as e:
		print(f"Error: {e}")
