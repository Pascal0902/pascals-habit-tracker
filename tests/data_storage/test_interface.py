import pytest
import sys
import os
from abc import ABC

# Add src to path for importing modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from data_storage.interface import StorageInterface
from habit_tracking.habits import Habit, UserHabit
from habit_tracking.users import User


class TestStorageInterface:
    """Test cases for the StorageInterface abstract class."""

    def test_storage_interface_is_abstract(self):
        """Test that StorageInterface cannot be instantiated directly."""
        with pytest.raises(TypeError):
            StorageInterface()

    def test_storage_interface_inheritance(self):
        """Test that StorageInterface inherits from ABC."""
        assert issubclass(StorageInterface, ABC)

    def test_abstract_methods_exist(self):
        """Test that all required abstract methods are defined."""
        expected_methods = [
            'insert_user',
            'update_user', 
            'delete_user',
            'get_user',
            'insert_habit',
            'update_habit',
            'delete_habit', 
            'get_habit',
            'get_all_habits',
            'insert_user_habit',
            'update_user_habit',
            'delete_user_habit',
            'get_user_habit',
            'get_all_user_habits'
        ]
        
        for method_name in expected_methods:
            assert hasattr(StorageInterface, method_name)
            method = getattr(StorageInterface, method_name)
            assert getattr(method, '__isabstractmethod__', False)

    def test_concrete_implementation_must_implement_all_methods(self):
        """Test that concrete implementations must implement all abstract methods."""
        
        # Create an incomplete implementation
        class IncompleteStorage(StorageInterface):
            def insert_user(self, user):
                pass
            # Missing other methods
        
        # Should not be able to instantiate
        with pytest.raises(TypeError):
            IncompleteStorage()

    def test_complete_implementation_can_be_instantiated(self):
        """Test that complete implementations can be instantiated."""
        
        class CompleteStorage(StorageInterface):
            def insert_user(self, user): return True
            def update_user(self, user): return True
            def delete_user(self, user): return True
            def get_user(self, username): return None
            def insert_habit(self, habit): return True
            def update_habit(self, habit): return True
            def delete_habit(self, habit): return True
            def get_habit(self, name): return None
            def get_all_habits(self): return []
            def insert_user_habit(self, user_habit): return True
            def update_user_habit(self, user_habit): return True
            def delete_user_habit(self, user_habit): return True
            def get_user_habit(self, userhabit_id): return None
            def get_all_user_habits(self): return []
        
        # Should be able to instantiate
        storage = CompleteStorage()
        assert isinstance(storage, StorageInterface)

    def test_method_signatures(self):
        """Test that abstract methods have correct signatures."""
        import inspect
        
        # Test user methods
        sig = inspect.signature(StorageInterface.insert_user)
        assert len(sig.parameters) == 2  # self, user
        
        sig = inspect.signature(StorageInterface.get_user)
        assert len(sig.parameters) == 2  # self, username
        
        # Test habit methods
        sig = inspect.signature(StorageInterface.insert_habit)
        assert len(sig.parameters) == 2  # self, habit
        
        sig = inspect.signature(StorageInterface.get_habit)
        assert len(sig.parameters) == 2  # self, name
        
        sig = inspect.signature(StorageInterface.get_all_habits)
        assert len(sig.parameters) == 1  # self
        
        # Test user_habit methods
        sig = inspect.signature(StorageInterface.insert_user_habit)
        assert len(sig.parameters) == 2  # self, user_habit
        
        sig = inspect.signature(StorageInterface.get_user_habit)
        assert len(sig.parameters) == 2  # self, userhabit_id
        
        sig = inspect.signature(StorageInterface.get_all_user_habits)
        assert len(sig.parameters) == 1  # self


if __name__ == '__main__':
    pytest.main([__file__])