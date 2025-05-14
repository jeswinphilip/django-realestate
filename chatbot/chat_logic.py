# chatbot/chat_logic.py

RESPONSES = {
    "greeting": "Hello! Welcome to Online Real Estate Platform Kerala. How can I assist you today?",
    "properties": "We have properties across Kerala including Kochi, Trivandrum, Kozhikode, Thrissur, and other major cities. Which location are you interested in?",
    "property_types": "We offer various property types including apartments, individual houses, villas, commercial spaces, and land plots. What type of property are you looking for?",
    "price": "Our properties range from ₹25 lakhs to ₹5 crores depending on location and property type. What's your budget range?",
    "locations": "We have properties in major Kerala cities including Kochi, Trivandrum, Kozhikode, Thrissur, Kollam, Palakkad, and more. Which area interests you?",
    "schedule_visit": "I'd be happy to arrange a property visit. Please provide your name, contact number, and preferred date and time for the visit.",
    "contact": "You can reach us at info@realestateportal.com or call +91 8590631262 for any inquiries.",
    "agents": "We have verified real estate agents across Kerala who can help you find the perfect property. Would you like to be connected with an agent?",
    "sell_property": "Looking to sell your property? You can list it on our platform by clicking on 'Sell Your Property' in the navigation menu and filling out the property details form. Our team will review and publish your listing within 24 hours.",
    "documents": "For property transactions, you'll need documents like title deed, encumbrance certificate, tax receipts, and identity proof. Do you need specific information about any document?",
    "loan": "We can help connect you with partner banks for home loans at competitive interest rates. Would you like more information about home loan options?",
    "registration": "Property registration in Kerala involves stamp duty (around 8-10% of property value) and registration fees. The exact process takes place at the Sub-Registrar office.",
    "amenities": "Our properties come with various amenities depending on the project, including swimming pools, gyms, 24/7 security, power backup, and more.",
    "about": "Online Real Estate Platform is Kerala's leading property portal connecting buyers, sellers, and agents in a convenient and secure environment.",
    "default": "I'm sorry, I didn't understand that. You can ask about properties in Kerala, pricing, locations, scheduling a visit, or contact information. How else can I assist you?"
}

def get_chatbot_response(user_input):
    user_input = user_input.lower().strip()
    
    # Check for specific queries about selling properties first (higher priority)
    if any(phrase in user_input for phrase in ["how to sell", "want to sell", "selling my", "list my property", "sell my"]):
        return RESPONSES["sell_property"]
    
    # Then check for greetings
    elif any(word in user_input for word in ["hello", "hi", "hey", "greetings", "namaste"]):
        return RESPONSES["greeting"]
    
    # Check for property queries - but now with more specific conditions to avoid false matches
    elif any(word in user_input for word in ["property", "properties", "house", "apartment", "flat", "villa"]):
        # Differentiate between buying and selling intent
        if any(word in user_input for word in ["sell", "selling", "list"]):
            return RESPONSES["sell_property"]
        elif "type" in user_input:
            return RESPONSES["property_types"]
        else:
            return RESPONSES["properties"]
    
    elif any(word in user_input for word in ["price", "cost", "budget", "rate", "value", "worth"]):
        return RESPONSES["price"]
    
    elif any(word in user_input for word in ["location", "place", "area", "city", "district", "where"]):
        return RESPONSES["locations"]
    
    elif any(word in user_input for word in ["schedule", "visit", "see", "tour", "viewing", "appointment"]):
        return RESPONSES["schedule_visit"]
    
    elif any(word in user_input for word in ["contact", "email", "phone", "number", "call", "reach"]):
        return RESPONSES["contact"]
    
    elif any(word in user_input for word in ["agent", "broker", "realtor", "consultant"]):
        return RESPONSES["agents"]
    
    # Now specifically check for "sell" as a standalone concept
    elif any(word in user_input for word in ["sell", "selling", "list", "listing"]):
        return RESPONSES["sell_property"]
    
    elif any(word in user_input for word in ["document", "papers", "certificate", "legal", "title"]):
        return RESPONSES["documents"]
    
    elif any(word in user_input for word in ["loan", "finance", "mortgage", "bank", "funding"]):
        return RESPONSES["loan"]
    
    elif any(word in user_input for word in ["registration", "register", "stamp duty", "legal process"]):
        return RESPONSES["registration"]
    
    elif any(word in user_input for word in ["amenities", "facilities", "features", "swimming", "gym"]):
        return RESPONSES["amenities"]
    
    elif any(word in user_input for word in ["about", "company", "platform", "website", "who"]):
        return RESPONSES["about"]
    
    else:
        return RESPONSES["default"]

# Additional function to handle complex queries
def handle_complex_query(user_input):
    user_input = user_input.lower()
    
    # Handle selling property queries with higher priority
    if "sell" in user_input and ("property" in user_input or "house" in user_input or "flat" in user_input):
        return RESPONSES["sell_property"]
    
    # Handle "how to" questions about selling
    elif "how" in user_input and "sell" in user_input:
        return RESPONSES["sell_property"]
    
    # Handle combination queries
    elif ("property" in user_input or "house" in user_input) and "kochi" in user_input:
        return "We have several properties in Kochi ranging from apartments in the city center to villas in suburban areas. Prices start from ₹45 lakhs. Would you like more specific information?"
    
    elif ("property" in user_input or "house" in user_input) and "trivandrum" in user_input:
        return "Our Trivandrum properties include apartments near Technopark, villas in Kovalam, and houses in Kazhakkoottam. Prices range from ₹35 lakhs to ₹2.5 crores."
    
    elif "budget" in user_input and "below" in user_input and any(str(num) for num in range(10, 100)):
        return "We have affordable properties under ₹50 lakhs in various locations across Kerala. These include 1-2 BHK apartments and small plots. Would you like to explore these options?"
    
    elif "luxury" in user_input or "premium" in user_input:
        return "Our premium properties include waterfront villas in Kochi, hillside estates in Munnar, and luxury apartments in major cities with amenities like private pools, smart home features, and exclusive club memberships."
    
    elif "investment" in user_input:
        return "Kerala offers excellent real estate investment opportunities, especially in growing cities like Kochi, Trivandrum, and Kozhikode. Would you like to speak with an investment advisor?"
    
    # Use the standard response system if no complex query is detected
    return get_chatbot_response(user_input)

# Main function to use in your views.py
def process_user_message(message):
    # Try complex query handling first
    response = handle_complex_query(message)
    
    # If it returns a default response, try the basic response system
    if response == RESPONSES["default"]:
        response = get_chatbot_response(message)
        
    return response