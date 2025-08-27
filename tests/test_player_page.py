"""Tests for player page scrapers."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
from player_page.main import ETL_player_profile
from player_page.ingest import PlayerProfilePageScraper


class TestPlayerPageScraper:
    """Test the PlayerProfilePageScraper class."""
    
    def test_ETL_player_profile(self):
        """Test the ETL_player_profile function."""
        # Mock dependencies
        mock_loader = Mock()
        mock_scraper = Mock()
        
        # Mock data
        mock_player_profile = pd.DataFrame({
            'player_id': ['MahoPa00'],
            'name': ['Patrick Mahomes'],
            'position': ['QB'],
            'height': ['6-3'],
            'weight': [225],
            'birth_date': ['1995-09-17'],
            'college': ['Texas Tech']
        })
        
        with patch('player_page.main.PlayerProfilePageScraper', return_value=mock_scraper):
            
            # Setup mocks
            mock_scraper.get_player_profile.return_value = mock_player_profile
            
            # Test the function
            ETL_player_profile('https://www.pro-football-reference.com/players/M/MahoPa00.htm', mock_loader)
            
            # Verify scraper was called correctly
            mock_scraper.load_page.assert_called_once_with('https://www.pro-football-reference.com/players/M/MahoPa00.htm')
            mock_scraper.get_player_profile.assert_called_once()
            
            # Verify loader was called correctly
            mock_loader.insert_player_profile_df.assert_called_once_with(mock_player_profile)
    
    def test_player_profile_data_structure(self):
        """Test that player profile data has expected structure."""
        # Mock the scraper
        with patch('player_page.main.PlayerProfilePageScraper') as mock_scraper_class:
            mock_scraper = Mock()
            mock_scraper.get_player_profile.return_value = pd.DataFrame({
                'player_id': ['MahoPa00'],
                'name': ['Patrick Mahomes'],
                'position': ['QB'],
                'height': ['6-3'],
                'weight': [225],
                'birth_date': ['1995-09-17'],
                'college': ['Texas Tech'],
                'draft_year': [2017],
                'draft_round': [1],
                'draft_pick': [10],
                'draft_team': ['KAN']
            })
            mock_scraper_class.return_value = mock_scraper
            
            # Test the function
            mock_loader = Mock()
            ETL_player_profile('https://example.com/player', mock_loader)
            
            # Verify the data structure
            called_data = mock_loader.insert_player_profile_df.call_args[0][0]
            assert isinstance(called_data, pd.DataFrame)
            assert not called_data.empty
            
            # Check for expected columns
            expected_columns = ['player_id', 'name', 'position']
            for col in expected_columns:
                assert col in called_data.columns


class TestPlayerDataValidation:
    """Test player data validation."""
    
    def test_player_id_format(self):
        """Test that player IDs follow expected format."""
        # Mock the scraper
        with patch('player_page.main.PlayerProfilePageScraper') as mock_scraper_class:
            mock_scraper = Mock()
            mock_scraper.get_player_profile.return_value = pd.DataFrame({
                'player_id': ['MahoPa00', 'BradyTo00', 'ChaseJa00']
            })
            mock_scraper_class.return_value = mock_scraper
            
            # Test the function
            mock_loader = Mock()
            ETL_player_profile('https://example.com/player', mock_loader)
            
            # Verify player IDs follow format (3 letters + 2 letters + 2 digits)
            called_data = mock_loader.insert_player_profile_df.call_args[0][0]
            for player_id in called_data['player_id']:
                assert len(player_id) == 7
                assert player_id[:3].isalpha()
                assert player_id[3:5].isalpha()
                assert player_id[5:].isdigit()
    
    def test_required_fields_present(self):
        """Test that required fields are present in player data."""
        # Mock the scraper
        with patch('player_page.main.PlayerProfilePageScraper') as mock_scraper_class:
            mock_scraper = Mock()
            mock_scraper.get_player_profile.return_value = pd.DataFrame({
                'player_id': ['MahoPa00'],
                'name': ['Patrick Mahomes'],
                'position': ['QB']
            })
            mock_scraper_class.return_value = mock_scraper
            
            # Test the function
            mock_loader = Mock()
            ETL_player_profile('https://example.com/player', mock_loader)
            
            # Verify required fields are present
            called_data = mock_loader.insert_player_profile_df.call_args[0][0]
            required_fields = ['player_id', 'name']
            for field in required_fields:
                assert field in called_data.columns
                assert not called_data[field].isna().all()  # Not all values are null


if __name__ == "__main__":
    pytest.main([__file__]) 