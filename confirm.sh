# ======================================================================
#
# Function: confirm
# Asks the user to confirm an action, If the user does not answer yes,
# then the script will immediately exit.
#
# Parameters:
# $@ - The confirmation message
#
# Examples:
# >  # Example 1
# >  # The preferred way to use confirm
# >  confirm Delete file1? && echo rm file1
# >  
# >  # Example 2
# >  # Use the $? variable to examine confirm's return value
# >  confirm Delete file2?
# >  if [ $? -eq 0 ]
# >  then
# >      echo Another file deleted
# >  fi
# >  
# >  # Example 3
# >  # Tell bash to exit right away if any command returns a non-zero code
# >  set -o errexit
# >  confirm Do you want to run the rest of the script?
# >  echo Here is the rest of the script
#
# ======================================================================

function confirm()
{
    echo -n "$@ "
    read -e answer
    for response in y Y yes YES Yes Sure sure SURE OK ok Ok
    do
        if [ "_$answer" == "_$response" ]
        then
            return 0
        fi
    done

    # Any answer other than the list above is considerred a "no" answer
    return 1
}

