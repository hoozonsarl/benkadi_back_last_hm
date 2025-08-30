#!/bin/bash

# =============================================================================
# SCRIPT DE GESTION DOCKER - BENKADI BLOOD
# =============================================================================
# Ce script permet de gérer facilement les services Docker du projet
# Benkadi Blood avec toutes les opérations courantes
# =============================================================================

set -e  # Arrêter le script en cas d'erreur

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="benkadi-blood"
COMPOSE_FILE="docker-compose.yml"

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE} BENKADI BLOOD - GESTIONNAIRE DOCKER${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker n'est pas installé ou n'est pas dans le PATH"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose n'est pas installé ou n'est pas dans le PATH"
        exit 1
    fi
}

wait_for_service() {
    local service=$1
    local max_attempts=30
    local attempt=0
    
    print_info "Attente du démarrage de $service..."
    
    while [ $attempt -lt $max_attempts ]; do
        if docker-compose ps | grep -q "$service.*Up"; then
            print_success "$service est démarré"
            return 0
        fi
        sleep 2
        attempt=$((attempt + 1))
        echo -n "."
    done
    
    print_error "$service n'a pas pu démarrer dans les temps"
    return 1
}

# =============================================================================
# FONCTIONS PRINCIPALES
# =============================================================================

# Démarrage rapide (sans rebuild)
start_quick() {
    print_info "Démarrage rapide de tous les services..."
    docker-compose up -d
    print_success "Tous les services sont démarrés!"
    show_services_info
}

# Démarrage complet avec rebuild total
start_all() {
    print_info "DÉMARRAGE COMPLET AVEC REBUILD - Cela peut prendre plusieurs minutes..."
    echo ""
    
    # 1. Arrêt complet et nettoyage
    print_info "1/10 - Arrêt des services existants..."
    docker-compose down -v 2>/dev/null || true
    
    # 2. Nettoyage des images et containers orphelins
    print_info "2/10 - Nettoyage des ressources Docker..."
    docker system prune -f
    
    # 3. Suppression des volumes de données (pour éviter conflits de credentials)
    print_info "3/10 - Nettoyage des données persistantes..."
    rm -rf db_data/ redis/ rabbitmq-data/ flower_data/ 2>/dev/null || true
    
    # 4. Construction complète des images
    print_info "4/10 - Construction des images Docker (--no-cache)..."
    docker-compose build --no-cache --pull
    
    # 5. Démarrage échelonné des services de base
    print_info "5/10 - Démarrage des services de base (PostgreSQL, Redis, RabbitMQ)..."
    docker-compose up -d db redis rabbitmq
    
    # 6. Attente de PostgreSQL avec vérification de santé
    print_info "6/10 - Attente de PostgreSQL (peut prendre jusqu'à 60s)..."
    local attempts=0
    local max_attempts=30
    while [ $attempts -lt $max_attempts ]; do
        if docker-compose exec db pg_isready -U benkadi -d benkadi_blood 2>/dev/null; then
            print_success "PostgreSQL est prêt!"
            break
        fi
        echo -n "."
        sleep 2
        attempts=$((attempts + 1))
    done
    
    if [ $attempts -eq $max_attempts ]; then
        print_error "PostgreSQL n'a pas démarré correctement"
        print_info "Vérifiez les logs: docker-compose logs db"
        exit 1
    fi
    
    # 7. Démarrage de l'application principale
    print_info "7/10 - Démarrage de l'application FastAPI..."
    docker-compose up -d app
    
    # 8. Attendre que l'app soit prête et exécuter les migrations
    print_info "8/10 - Attente de l'application et exécution des migrations..."
    sleep 10
    
    # Vérifier si des migrations existent, sinon les créer
    if ! docker-compose exec app alembic current 2>/dev/null; then
        print_info "Création de la première migration..."
        docker-compose exec app alembic revision --autogenerate -m "Initial migration"
    fi
    
    docker-compose exec app alembic upgrade head
    
    # 9. Démarrage des services Celery
    print_info "9/10 - Démarrage des services Celery (Worker, Beat)..."
    docker-compose up -d celery-worker celery-beat
    
    # 10. Démarrage des outils de monitoring
    print_info "10/10 - Démarrage des outils de monitoring (PgAdmin, Flower)..."
    docker-compose up -d pgadmin4 flower
    
    # Vérification finale
    sleep 5
    print_info "Vérification finale des services..."
    if docker-compose ps | grep -q "Up"; then
        print_success "✨ DÉMARRAGE COMPLET TERMINÉ AVEC SUCCÈS!"
        echo ""
        show_services_info
        echo ""
        print_info "💡 Conseils:"
        print_info "   - Attendez quelques secondes avant d'accéder aux services"
        print_info "   - Vérifiez les logs si un service ne répond pas: ./docker-manager.sh logs [service]"
        print_info "   - Pour un redémarrage rapide ultérieur, utilisez: ./docker-manager.sh quick"
    else
        print_error "Certains services n'ont pas démarré correctement"
        print_info "Vérifiez le statut avec: ./docker-manager.sh status"
    fi
}

# Arrêt complet
stop_all() {
    print_info "Arrêt de tous les services..."
    docker-compose down
    print_success "Tous les services sont arrêtés"
}

# Arrêt avec suppression des volumes (ATTENTION: efface les données)
stop_clean() {
    print_warning "ATTENTION: Cette opération va supprimer toutes les données!"
    read -p "Êtes-vous sûr? (yes/no): " confirm
    
    if [[ $confirm == "yes" ]]; then
        print_info "Arrêt et nettoyage complet..."
        docker-compose down -v
        docker system prune -f
        print_success "Nettoyage terminé"
    else
        print_info "Opération annulée"
    fi
}

# Redémarrage
restart_all() {
    print_info "Redémarrage de tous les services..."
    stop_all
    start_all
}

# Mise à jour du projet
update_project() {
    print_info "Mise à jour du projet..."
    
    # 1. Arrêter les services
    docker-compose down
    
    # 2. Reconstruire les images
    print_info "Reconstruction des images..."
    docker-compose build --no-cache
    
    # 3. Redémarrer
    start_all
    
    print_success "Mise à jour terminée"
}

# Gestion des migrations de base de données
manage_db() {
    case $1 in
        "migrate")
            print_info "Exécution des migrations..."
            docker-compose exec app alembic upgrade head
            print_success "Migrations appliquées"
            ;;
        "create")
            if [ -z "$2" ]; then
                print_error "Nom de migration requis: ./docker-manager.sh db create 'nom_migration'"
                exit 1
            fi
            print_info "Création d'une nouvelle migration: $2"
            docker-compose exec app alembic revision --autogenerate -m "$2"
            print_success "Migration créée"
            ;;
        "rollback")
            print_info "Rollback de la dernière migration..."
            docker-compose exec app alembic downgrade -1
            print_success "Rollback effectué"
            ;;
        "reset")
            print_warning "ATTENTION: Cette opération va réinitialiser la base de données!"
            read -p "Êtes-vous sûr? (yes/no): " confirm
            if [[ $confirm == "yes" ]]; then
                docker-compose down
                rm -rf db_data/
                docker-compose up -d db
                sleep 10
                docker-compose up -d app
                sleep 5
                docker-compose exec app alembic upgrade head
                print_success "Base de données réinitialisée"
            fi
            ;;
        *)
            echo "Commandes DB disponibles:"
            echo "  migrate  - Appliquer les migrations"
            echo "  create   - Créer une nouvelle migration"
            echo "  rollback - Annuler la dernière migration"
            echo "  reset    - Réinitialiser la DB (ATTENTION: efface tout)"
            ;;
    esac
}

# Affichage des logs
show_logs() {
    if [ -z "$1" ]; then
        print_info "Affichage des logs de tous les services..."
        docker-compose logs -f
    else
        print_info "Affichage des logs du service: $1"
        docker-compose logs -f "$1"
    fi
}

# Statut des services
show_status() {
    print_info "Statut des services:"
    docker-compose ps
    echo ""
    print_info "Utilisation des ressources:"
    docker stats --no-stream
}

# Informations des services
show_services_info() {
    echo ""
    print_info "Services disponibles:"
    echo "  🌐 API Documentation: http://localhost:8081/docs"
    echo "  🐘 PgAdmin: http://localhost:5050 (benkadihm@gmail.com / benhm20Pass)"
    echo "  🌸 Flower (Celery): http://localhost:5555 (benkadi@gmail.com / 6775212952)"
    echo "  📊 Application: http://localhost:8081"
    echo ""
    print_info "Connexions base de données:"
    echo "  Host: localhost"
    echo "  Port: 8001"
    echo "  Database: benkadi_blood"
    echo "  User: benkadi"
    echo "  Password: ben20Pass"
}

# Sauvegarde de la base de données
backup_db() {
    local backup_file="backup_$(date +%Y%m%d_%H%M%S).sql"
    print_info "Création d'une sauvegarde: $backup_file"
    
    docker-compose exec db pg_dump -U benkadi benkadi_blood > "$backup_file"
    print_success "Sauvegarde créée: $backup_file"
}

# Restauration de la base de données
restore_db() {
    if [ -z "$1" ]; then
        print_error "Fichier de sauvegarde requis: ./docker-manager.sh restore backup.sql"
        exit 1
    fi
    
    if [ ! -f "$1" ]; then
        print_error "Fichier de sauvegarde introuvable: $1"
        exit 1
    fi
    
    print_warning "ATTENTION: Cette opération va écraser la base de données existante!"
    read -p "Êtes-vous sûr? (yes/no): " confirm
    
    if [[ $confirm == "yes" ]]; then
        print_info "Restauration de la base de données..."
        docker-compose exec -T db psql -U benkadi -d benkadi_blood < "$1"
        print_success "Base de données restaurée"
    fi
}

# Tests
run_tests() {
    print_info "Exécution des tests..."
    docker-compose exec app pytest
    print_success "Tests terminés"
}

# Shell interactif dans un container
shell() {
    local service=${1:-app}
    print_info "Ouverture d'un shell dans le service: $service"
    docker-compose exec "$service" /bin/bash
}

# =============================================================================
# MENU PRINCIPAL
# =============================================================================

show_help() {
    cat << EOF
Usage: $0 [COMMAND] [OPTIONS]

COMMANDES PRINCIPALES:
  start       - Démarrage complet avec rebuild (première installation)
  quick       - Démarrage rapide (services déjà configurés)
  stop        - Arrêter tous les services
  restart     - Redémarrer tous les services
  update      - Mettre à jour le projet
  clean       - Arrêt et nettoyage complet (SUPPRIME LES DONNÉES!)

GESTION BASE DE DONNÉES:
  db migrate           - Appliquer les migrations
  db create <name>     - Créer une nouvelle migration
  db rollback          - Annuler la dernière migration
  db reset             - Réinitialiser la DB (SUPPRIME TOUT!)

MONITORING:
  status      - Afficher le statut des services
  logs [service] - Afficher les logs (tous ou d'un service spécifique)
  info        - Afficher les informations de connexion

OUTILS:
  backup      - Sauvegarder la base de données
  restore <file> - Restaurer la base de données
  test        - Exécuter les tests
  shell [service] - Ouvrir un shell (défaut: app)

EXEMPLES:
  $0 start
  $0 db create "add_new_table"
  $0 logs app
  $0 backup
  $0 restore backup_20240830_143022.sql

EOF
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    print_header
    check_docker
    
    case "${1:-help}" in
        "start")
            start_all
            ;;
        "quick")
            start_quick
            ;;
        "stop")
            stop_all
            ;;
        "restart")
            restart_all
            ;;
        "update")
            update_project
            ;;
        "clean")
            stop_clean
            ;;
        "db")
            manage_db "${2:-help}" "$3"
            ;;
        "status")
            show_status
            ;;
        "logs")
            show_logs "$2"
            ;;
        "info")
            show_services_info
            ;;
        "backup")
            backup_db
            ;;
        "restore")
            restore_db "$2"
            ;;
        "test")
            run_tests
            ;;
        "shell")
            shell "$2"
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Exécution du script principal
main "$@"