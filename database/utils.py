

import re
import unicodedata


def   calculate_checksum(value: str ) -> int:
        """Calculates and returns the checksum for EAN13-Code.

        Calculates the checksum for the supplied `value` (if any) or for this barcode's
        internal ``self.ean`` property.
        """

        ean_without_checksum = value
        evensum = sum(int(x) for x in ean_without_checksum[-2::-2])
        oddsum = sum(int(x) for x in ean_without_checksum[-1::-2])
        return (10 - ((evensum + oddsum * 3) % 10)) % 10




def generate_username(nom: str, prenom: str) -> str:
    """
    Generate a username by combining a person's first and last name.
    
    This function:
    1. Concatenates the last name and first name
    2. Converts to lowercase
    3. Removes all spaces
    4. Removes all special characters while preserving alphanumeric characters
    5. Keeps numbers intact
    
    Args:
        nom: The person's last name
        prenom: The person's first name
    
    Returns:
        A clean username string with only alphanumeric characters
    
    Example:
        generate_username("Müller-Thompson", "Jean-François") -> "mullerthompsonjeanfrancois"
        generate_username("Smith", "Junior 2") -> "smithjunior2"
    """
    # Step 1: Concatenate the names
    full_name = f"{nom}{prenom}"
    
    # Step 2: Convert to lowercase
    full_name = full_name.lower()
    
    # Step 3: Normalize Unicode characters (handle accents)
    # This converts accented characters to their non-accented equivalents
    normalized = unicodedata.normalize('NFKD', full_name)
    full_name = ''.join([c for c in normalized if not unicodedata.combining(c)])
    
    # Step 4: Remove all non-alphanumeric characters
    # This pattern matches any character that is NOT a-z or 0-9
    clean_name = re.sub(r'[^a-z0-9]', '', full_name)
    
    return clean_name