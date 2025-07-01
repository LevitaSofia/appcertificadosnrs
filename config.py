#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configurações para execução em produção/rede
Sistema de Treinamentos NR
"""

import os
from datetime import timedelta

class Config:
    """Configurações base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-muito-segura-aqui-2025'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///certificados.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/imagens'
    VIDEOS_FOLDER = 'static/videos'
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB máximo por arquivo
    
    # Configurações de sessão
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)  # Sessão expira em 8 horas
    SESSION_COOKIE_SECURE = False  # True apenas para HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class DevelopmentConfig(Config):
    """Configurações de desenvolvimento"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configurações de produção"""
    DEBUG = False
    TESTING = False
    
    # Configurações de segurança para produção
    SESSION_COOKIE_SECURE = True  # Apenas para HTTPS
    WTF_CSRF_ENABLED = True

class NetworkConfig(Config):
    """Configurações para rede local"""
    DEBUG = True  # Manter debug para rede local
    TESTING = False
    
    # Configurações otimizadas para rede
    THREADED = True
    HOST = '0.0.0.0'  # Permite conexões de qualquer IP
    PORT = 5000

# Configuração padrão
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'network': NetworkConfig,
    'default': NetworkConfig
}
