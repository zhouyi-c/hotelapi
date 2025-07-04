from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from ..services.complaint_service import ComplaintService
from ..models.schemas import ComplaintCreate

class ComplaintAgent(BaseAgent):
    """AI agent for handling customer complaints."""
    
    def __init__(self):
        super().__init__(
            name="complaint_agent",
            description="Handles customer complaints and provides resolutions"
        )
        self.complaint_service = ComplaintService()
    
    async def process(self, input_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a customer complaint and provide a resolution.
        
        Args:
            input_data: Should contain 'subject' and 'description' of the complaint
            context: Additional context (e.g., user information)
            
        Returns:
            Dictionary containing the agent's response
        """
        try:
            # Create a new complaint
            complaint = ComplaintCreate(
                subject=input_data.get('subject', 'No subject'),
                description=input_data.get('description', ''),
                customer_email=context.get('customer_email', '') if context else '',
                priority=input_data.get('priority', 'medium')
            )
            
            # Save the complaint
            created_complaint = await self.complaint_service.create_complaint(complaint)
            
            # Generate a response (in a real app, this would use an LLM)
            response = {
                'status': 'received',
                'message': 'Your complaint has been received and is being processed.',
                'complaint_id': created_complaint.id,
                'estimated_resolution_time': '24-48 hours',
                'suggested_solutions': [
                    'Check our FAQ section for immediate answers',
                    'A customer service representative will contact you shortly',
                    'You can track your complaint status using the provided ID'
                ]
            }
            
            # Update memory with the complaint details
            self.update_memory(f'complaint_{created_complaint.id}', {
                'status': 'received',
                'timestamp': created_complaint.created_at.isoformat(),
                'customer': context.get('customer_email', '') if context else ''
            })
            
            return response
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to process complaint: {str(e)}'
            }
    
    async def get_complaint_status(self, complaint_id: int) -> Dict[str, Any]:
        """Get the status of a complaint."""
        complaint = await self.complaint_service.get_complaint(complaint_id)
        if not complaint:
            return {
                'status': 'not_found',
                'message': f'No complaint found with ID {complaint_id}'
            }
        
        return {
            'status': 'success',
            'complaint_id': complaint.id,
            'status': complaint.status,
            'created_at': complaint.created_at.isoformat(),
            'updated_at': complaint.updated_at.isoformat() if hasattr(complaint, 'updated_at') else None
        }
