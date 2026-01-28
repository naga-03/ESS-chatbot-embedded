from typing import Dict, Any
from src.auth import AuthManager
from src.intent_detector import IntentDetector
from src.entity_extractor import EntityExtractor
from src.business_logic import BusinessLogicHandler
from src.response_generator import LLMResponseGenerator
from src.admin_email_feature import handle_admin_email_feature


class ESSChatbot:
    """Main chatbot orchestrator for Employee Self-Service."""

    def __init__(
        self,
        employees_file: str = "data/employees.json",
        intents_file: str = "config/intents.json",
        gemini_model: str = "gemini-2.5-flash-lite"
    ):
        self.auth_manager = AuthManager(employees_file)
        self.intent_detector = IntentDetector(intents_file)
        self.entity_extractor = EntityExtractor()
        self.business_logic = BusinessLogicHandler(employees_file)
        self.response_generator = LLMResponseGenerator(gemini_model)

        # Central conversation state
        self.conversation_state: Dict[str, Any] = {}

    # =====================================================
    # ENTRY POINT
    # =====================================================
    def process_message(self, user_input: str) -> Dict[str, Any]:
        command = user_input.lower().strip()

        if command.startswith("/login"):
            return self._handle_login_command(command)

        if command == "/logout":
            return self._handle_logout_command()

        if command == "/help":
            return self._handle_help_command()

        if command == "/status":
            return self._handle_status_command()

        return self._process_query(user_input)

    # =====================================================
    # CORE PROCESSING
    # =====================================================
    def _process_query(self, query: str) -> Dict[str, Any]:

        # 🔒 HARD ADMIN EMAIL MODE
        if self.conversation_state.get("admin_email_active") is True:
            user_data = self.auth_manager.get_current_user()

            admin_message = handle_admin_email_feature(
                user_data,
                {"raw_text": query}
            )

            # Exit admin email mode after success
            if admin_message.startswith("✅"):
                self.conversation_state.pop("admin_email_active", None)

            return {
                "success": True,
                "intent": "ADMIN_SEND_EMAIL",
                "intent_name": "Admin Send Email",
                "confidence": 1.0,
                "entities": {},
                "message": admin_message,
                "requires_auth": True,
                "system_response": True
            }

        # -------------------------------------------------
        # INTENT DETECTION
        # -------------------------------------------------
        intent, confidence = self.intent_detector.get_intent(query, threshold=0.5)

        if intent is None:
            return self._fallback_response(query)

        intent_id = intent["intent_id"]

        entities = self.entity_extractor.extract_entities(query)
        entities["raw_text"] = query

        # -------------------------------------------------
        # AUTH CHECK
        # -------------------------------------------------
        if self.intent_detector.is_private_intent(intent_id) and not self.auth_manager.is_authenticated():
            return {
                "success": False,
                "intent": intent_id,
                "entities": entities,
                "message": "This information is private. Please login using /login <employee_id> <password>",
                "requires_auth": True
            }

        user_data = self.auth_manager.get_current_user() if self.auth_manager.is_authenticated() else None

        # -------------------------------------------------
        # START ADMIN EMAIL FLOW
        # -------------------------------------------------
        if intent_id == "ADMIN_SEND_EMAIL":
            admin_message = handle_admin_email_feature(user_data, entities)

            # Lock admin email mode safely (NO emoji dependency)
            self.conversation_state["admin_email_active"] = True

            return {
                "success": True,
                "intent": intent_id,
                "intent_name": intent.get("name"),
                "confidence": float(confidence),
                "entities": entities,
                "message": admin_message,
                "requires_auth": True,
                "system_response": True
            }

        # -------------------------------------------------
        # NORMAL BUSINESS LOGIC
        # -------------------------------------------------
        business_response = (
            self.business_logic.handle_intent(
                intent_id,
                self.auth_manager,
                query,
                entities,
                self.conversation_state
            ) or {}
        )

        final_message = self.response_generator.generate_response(
            intent,
            entities,
            user_data,
            self.conversation_state
        )

        # Reset state unless next action exists
        if not business_response.get("data", {}).get("next_action"):
            self.conversation_state.clear()

        return {
            "success": business_response.get("success", True),
            "intent": intent_id,
            "intent_name": intent.get("name"),
            "confidence": float(confidence),
            "entities": entities,
            "data": business_response.get("data"),
            "message": final_message,
            "requires_auth": self.intent_detector.is_private_intent(intent_id)
        }

    # =====================================================
    # FALLBACK
    # =====================================================
    def _fallback_response(self, query: str) -> Dict[str, Any]:
        response = self.response_generator.generate_response(
            {"intent_id": "general_inquiry", "name": "General Inquiry"},
            {},
            self.auth_manager.get_current_user() if self.auth_manager.is_authenticated() else None,
            {}
        )
        return {
            "success": True,
            "intent": "general_inquiry",
            "entities": {},
            "message": response,
            "requires_auth": False
        }

    # =====================================================
    # COMMAND HANDLERS
    # =====================================================
    def _handle_login_command(self, command: str) -> Dict[str, Any]:
        parts = command.split()
        if len(parts) < 3:
            return {"success": False, "message": "Usage: /login <employee_id> <password>"}

        success, message = self.auth_manager.login(parts[1], parts[2])
        return {"success": success, "message": message}

    def _handle_logout_command(self) -> Dict[str, Any]:
        success, message = self.auth_manager.logout()
        return {"success": success, "message": message}

    def _handle_status_command(self) -> Dict[str, Any]:
        if self.auth_manager.is_authenticated():
            user = self.auth_manager.get_current_user()
            return {"success": True, "message": f"Logged in as {user['name']} ({user['employee_id']})"}
        return {"success": True, "message": "Not logged in."}

    def _handle_help_command(self) -> Dict[str, Any]:
        return {
            "success": True,
            "message": (
                "Commands:\n"
                "/login <id> <password>\n"
                "/logout\n"
                "/status\n"
                "/help\n"
            )
        }
