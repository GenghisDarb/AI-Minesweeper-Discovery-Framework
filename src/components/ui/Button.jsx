import React from 'react';
import PropTypes from 'prop-types';

const Button = ({ variant = 'default', children, ...props }) => {
  const baseStyles = 'px-4 py-2 font-semibold rounded';
  const variants = {
    default: 'bg-primary text-primary-foreground hover:bg-primary-dark',
    outline: 'border border-primary text-primary hover:bg-primary-light',
    destructive: 'bg-red-500 text-white hover:bg-red-600',
  };

  return (
    <button className={`${baseStyles} ${variants[variant]}`} {...props}>
      {children}
    </button>
  );
};

Button.propTypes = {
  variant: PropTypes.oneOf(['default', 'outline', 'destructive']),
  children: PropTypes.node.isRequired,
};

export default Button;
