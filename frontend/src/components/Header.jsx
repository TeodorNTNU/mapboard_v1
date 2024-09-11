import React, { useState, useRef, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars, faWifi, faBolt, faMoon, faCog, faFilePdf } from '@fortawesome/free-solid-svg-icons';
import { IconButton } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
//import Uploader from './Uploader'; // Adjusted path to match the structure

const Header = ({ }) => {
  const [menuOpen, setMenuOpen] = useState(false);
  const [isUploaderOpen, setUploaderOpen] = useState(false);
  const menuRef = useRef();

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  const toggleUploader = () => {
    setUploaderOpen(!isUploaderOpen);
    setMenuOpen(false);
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuOpen(false);
      }
    };

    if (menuOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    } else {
      document.removeEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [menuOpen]);

  return (
    <div className="header-container">
      <header className="header-row">
        <button className="menu-icon" onClick={toggleMenu}>
          <FontAwesomeIcon icon={faBars} />
        </button>

      </header>

      {menuOpen && (
        <div ref={menuRef} className="popup-menu">
          <div className="menu-item" onClick={toggleUploader}>
            <FontAwesomeIcon icon={faFilePdf} />
            <span>PDF-uploader</span>
          </div>
          <div className="menu-item">
            <FontAwesomeIcon icon={faCog} />
            <span>Settings</span>
          </div>
          <div className="menu-item">
            <FontAwesomeIcon icon={faBolt} />
            <span>Power Mode</span>
          </div>
          <div className="menu-item">
            <FontAwesomeIcon icon={faMoon} />
            <span>Night Light</span>
          </div>
        </div>
      )}

      {isUploaderOpen && (
        <div className="uploader-modal">
          <div className="uploader-modal-content">
            <button className="close-btn" onClick={toggleUploader}>X</button>
            <Uploader />
          </div>
        </div>
      )}
    </div>
  );
};

export default Header;
